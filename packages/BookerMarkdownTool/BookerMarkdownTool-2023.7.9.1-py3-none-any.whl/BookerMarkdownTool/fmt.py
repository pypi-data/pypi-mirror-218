import re
import os
import copy
from multiprocessing import Pool
from os import path
from pyquery import PyQuery as pq
from .util import *

def fmt_zh(text):
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9_])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9_])([\u4e00-\u9fff])', r'\1 \2', text)
    return text

def fmt_packt(html):
    RE_UNUSED_TAG = r'</?(article|section|span|header|link)[^>]*>'
    RE_DIV_START = r'<div[^>]*>\s*'
    RE_DIV_CONT = r'<div>([^<][\s\S]+?)</div>'
    RE_REPL_P = r'<p>\1</p>'
    RE_P_SNIPPLET = r'<p [^>]*class=".*?\bsnippet\b.*?"[^>]*>(.+?)</p>'
    RE_P_SRC_CODE = r'<p [^>]*class=".*?\bsource-code\b.*?"[^>]*>(.+?)</p>'
    RE_REPL_PRE = r'<pre>\1</pre>'
    RE_REPL_CODE = r'<code>\1</code>'
    RE_STRONG_INLINE = r'<strong [^>]*class=".*?\binline-code\b.*?"[^>]*>(.+?)</strong>'
    RE_STRONG_CODE = r'<strong [^>]*class=".*?\binline\b.*?"[^>]*>(.+?)</strong>'
    RE_PRE_NL = r'</pre>\s*<pre>'
    RE_SRC = r'src="(.+?)"'
    # 去除无用标签
    html = re.sub(RE_UNUSED_TAG, '', html)
    # DIV 内容
    html = re.sub(RE_DIV_START, '<div>', html)
    html = re.sub(RE_DIV_CONT, RE_REPL_P, html)
    # 代码段
    html = re.sub(RE_P_SRC_CODE, RE_REPL_PRE, html)
    html = re.sub(RE_P_SNIPPLET, RE_REPL_PRE, html)
    html = re.sub(RE_STRONG_INLINE, RE_REPL_CODE, html)
    html = re.sub(RE_STRONG_CODE, RE_REPL_CODE, html)
    html = re.sub(RE_PRE_NL, '\n', html)
    # 图像
    def img_src_repl(m):
        src = m.group(1)
        fname = path.basename(src)
        return f'src="img/{fname}"'
    html = re.sub(RE_SRC, img_src_repl, html)
    return html
    
def process_apress_pre(el_pre, root):
    el_lines = el_pre.find('.FixedLine')
    lines = []
    for i in range(len(el_lines)):
        el_line = el_lines.eq(i)
        lines.append(el_line.text())
    el_new_pre = root('<pre></pre>')
    code = re.sub(r'<[^>]*>', '', '\n'.join(lines))
    code = re.sub(r'^\x20+', '', code, flags= re.M)
    el_new_pre.text(code)
    el_pre.replace_with(el_new_pre)

def process_apress_para(el_para, root):
    el_new_para = root('<p></p>')
    el_new_para.html(el_para.html())
    el_para.replace_with(el_new_para)

def fmt_apress(html):
    html = html.replace('<?xml version="1.0" encoding="utf-8"?>', '')
    html = re.sub(r'xmlns=".+?"', '', html)
    html = re.sub(r'xmlns:epub=".+?"', '', html)
    root = pq(html)
    
    el_pres = root('.ProgramCode')
    for i in range(len(el_pres)):
        el_pre = el_pres.eq(i)
        el_new_pre = root('<pre></pre>')
        code = re.sub(r'<[^>]*>', '', el_pre.text())
        code = re.sub(r'^\x20+', '', code, flags=re.M)
        code = code.replace('\xa0', '\x20')
        el_new_pre.text(code)
        el_pre.replace_with(el_new_pre)
    
    el_codes = root('.EmphasisFontCategoryNonProportional, .FontName2, .FontName1')
    for i in range(len(el_codes)):
        el_code = el_codes.eq(i)
        el_new_code = root('<code></code>')
        el_new_code.text(el_code.text())
        el_code.replace_with(el_new_code)
        
    el_paras = root('div.Para')
    print(len(el_paras))
    for i in range(len(el_paras)):
        process_apress_para(el_paras.eq(i), root)
        
    el_lis = root('.UnorderedList, .OrderedList, pre, .Figure, .Table')
    print(len(el_lis))
    for i in range(len(el_lis)):
        el_li = el_lis.eq(i)
        el_li_parent = el_li.parent()
        if not el_li_parent.is_('p, div.Para'):
            continue
        el_li.remove()
        el_li_parent.after(el_li)
        
    el_paras = root('.CaptionNumber, .MediaObject')
    print(len(el_paras))
    for i in range(len(el_paras)):
        process_apress_para(el_paras.eq(i), root)
    
    root('.ChapterContextInformation, .AuthorGroup, .ItemNumber').remove()
    
    html = str(root)
    html = re.sub(r'</?(div|span|article|header|section|figure|figcaption)[^>]*>', '', html)
    return html


def fmt_dir(args):
    dir = args.fname
    fnames = os.listdir(dir)
    pool = Pool(args.threads)
    for fname in fnames:
        args = copy.deepcopy(args)
        args.fname = path.join(dir, fname)
        pool.apply_async(fmt_file, [args])
    pool.close()
    pool.join()
    
# @safe()
def fmt_file(args):
    mode = args.mode
    if not args.fname.endswith('.html') and \
        not args.fname.endswith('.md'):
        print('请提供 HTML 或 MD 文件')
        return
    print(args.fname)
    text = open(args.fname, encoding='utf8').read()
    if mode == 'zh':
        text = fmt_zh(text)
    elif mode == 'packt':
        text = fmt_packt(text)
    elif mode == 'apress':
        text = fmt_apress(text)
    open(args.fname, 'w', encoding='utf8').write(text)

def fmt_handle(args):
    if path.isdir(args.fname):
        fmt_dir(args)
    else:
        fmt_file(args)