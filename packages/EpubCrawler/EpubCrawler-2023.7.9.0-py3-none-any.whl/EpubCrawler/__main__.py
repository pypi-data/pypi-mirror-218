#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from urllib.parse import urljoin
import sys
import json
import yaml
import warnings
from pyquery import PyQuery as pq
import time
from os import path
import re
from concurrent.futures import ThreadPoolExecutor
import hashlib
from readability import Document
from GenEpub import gen_epub
from . import *
from .util import *
from .img import *
from .config import config
from .sele_crawler import crawl_sele
from .common import *

warnings.filterwarnings("ignore")

def get_toc_from_cfg():
    if config['list'] and len(config['list']) > 0:
        return config['list']
        
    if not config['url']:
        print('URL not specified')
        sys.exit()
        
    html = request_retry(
        'GET', config['url'],
        retry=config['retry'],
        check_status=config['checkStatus'],
        headers=config['headers'],
        timeout=config['timeout'],
        proxies=config['proxy'],
        verify=False,
    ).content.decode(config['encoding'], 'ignore')
    return get_toc(html, config['url'])
    
def get_toc(html, base):
    root = pq(html)
    
    if config['remove']:
        root(config['remove']).remove()
        
    el_links = root(config['link'])
    vis = set()
    
    res = []
    for i in range(len(el_links)):
        el_link = el_links.eq(i)
        url = el_link.attr('href')
        if not url:
            text = el_link.text().strip()
            res.append(text)
            continue
            
        url = re.sub(r'#.*$', '', url)
        if base:
            url = urljoin(base, url)
        if not url.startswith('http'):
            continue
        if url in vis: continue
        vis.add(url)
        res.append(url)
        
    return res

    
def tr_download_page_safe(url, art, imgs):
    try:
        tr_download_page(url, art, imgs)
    except Exception as ex:
        print(f'{url} 下载失败：{ex}')

def tr_download_page(url, art, imgs):
    hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache = load_article(hash)
    if cache is not None and config['cache']:
        print(f'{url} 已存在于本地缓存中')
        art.update(cache)
        art['content'] = process_img(
            art['content'], imgs,
            page_url=url,
            img_prefix='../Images/',
        )
        return
    for i in range(config['retry']):
        html = request_retry(
            'GET', url,
            retry=config['retry'],
            check_status=config['checkStatus'],
            headers=config['headers'],
            timeout=config['timeout'],
            proxies=config['proxy'],
            verify=False,
        ).content.decode(config['encoding'], 'ignore')
        r = get_article(html, url)
        if not config['checkBlank'] or \
           (r['title'] and r['content']):
           break
        if i == config['retry'] - 1:
            raise Exception(f'{url} 标题或内容为空')
    art.update(r)
    save_article(hash, art)
    art['content'] = process_img(
        art['content'], imgs,
        page_url=url,
        img_prefix='../Images/',
    )
    print(f'{url} 下载成功')
    time.sleep(config['wait'])
    

def update_config(cfg_fname, user_cfg):
    global get_toc
    global get_article
    
    config.update(user_cfg)
    
    if not config['title']:
        config['title'] = 'title'
    
    if config['proxy']:
        proxies = {
            'http': config['proxy'],
            'https': config['proxy'],
        }
        config['proxy'] = proxies
    
    set_img_pool(ThreadPoolExecutor(config['imgThreads']))
    
    if config['external']:
        ex_fname = path.join(path.dirname(cfg_fname), config['external'])
        mod = load_module(ex_fname)
        get_toc = getattr(mod, 'get_toc', get_toc)
        get_article = getattr(mod, 'get_article', get_article)
        
    if not config['timeout']:
        config['timeout'] = (
            config['connTimeout'],
            config['readTimeout'],
        )


def main():
    cfg_fname = sys.argv[1] \
        if len(sys.argv) > 1 \
        else 'config.json'
    if not path.exists(cfg_fname):
        print('please provide config file')
        return
    
    ext = extname(cfg_fname).lower()
    cont = open(cfg_fname, encoding='utf-8').read()
    if ext == 'json':
        user_cfg = json.loads(cont)
    elif ext in ['yaml', 'yml']:
        user_cfg = yaml.safe_load(cont)
    elif ext == 'txt':
        urls = [l.strip() for l in cont.split('\n')]
        urls = [l for l in urls if l]
        name = re.sub('\.\w+$', '', path.basename(cfg_fname))
        user_cfg = {
            'name': name,
            'url': urls[0] if urls else '',
            'list': urls,
        }
    else:
        print('配置文件必须为 JSON、YAML 或 TXT')
        return
    update_config(cfg_fname, user_cfg)
    
    if config['selenium']: 
        crawl_sele()
        return
    
    toc = get_toc_from_cfg()
    articles = []
    imgs = {}
    if config['name']:
        articles.append({
            'title': config['name'],
            'content': f"<p>来源：<a href='{config['url']}'>{config['url']}</a></p>",
        })
    
    text_pool = ThreadPoolExecutor(config['textThreads'])
    hdls = []
    for url in toc:
        print(f'page: {url}')
        if not re.search(r'^https?://', url):
            articles.append({'title': url, 'content': ''})
            continue
        
        art = {}
        articles.append(art)
        hdl = text_pool.submit(tr_download_page_safe, url, art, imgs)
        hdls.append(hdl)
            
        
    for h in hdls: h.result()
    articles = [art for art in articles if art]
    gen_epub(articles, imgs, limit=config['sizeLimit'])
    print('done...')
    
if __name__ == '__main__': main()
    