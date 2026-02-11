#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析天舟.wcp文件，提取目录结构
"""

import re

def parse_wcp_file(file_path):
    """解析wcp文件，返回目录结构"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("文件读取成功，长度:", len(content))
    
    # 提取[TOPICS]部分
    topics_section = re.search(r'\[TOPICS\](.*?)(?=\[|$)', content, re.DOTALL)
    if not topics_section:
        print("未找到[TOPICS]部分")
        return []
    
    topics_content = topics_section.group(1)
    print("[TOPICS]部分提取成功，长度:", len(topics_content))
    
    # 提取标题数量
    title_list_match = re.search(r'TitleList=(\d+)', topics_content)
    if not title_list_match:
        print("未找到TitleList数量")
        return []
    
    title_count = int(title_list_match.group(1))
    print("标题数量:", title_count)
    
    # 提取每个标题的信息
    titles = []
    for i in range(title_count):
        title_match = re.search(rf'TitleList\.Title\.{i}=(.*?)\n', topics_content)
        level_match = re.search(rf'TitleList\.Level\.{i}=(.*?)\n', topics_content)
        url_match = re.search(rf'TitleList\.Url\.{i}=(.*?)\n', topics_content)
        
        if title_match and level_match:
            title = title_match.group(1)
            level = int(level_match.group(1))
            url = url_match.group(1) if url_match else ''
            
            titles.append({
                'title': title,
                'level': level,
                'url': url
            })
            if i < 10:  # 只打印前10个标题
                print(f"标题{i}: {title}, 级别: {level}, URL: {url}")
    
    print("提取到的标题数量:", len(titles))
    return titles

def build_tree(titles):
    """将扁平的标题列表构建成树形结构"""
    tree = []
    stack = []
    
    for item in titles:
        title = item['title']
        level = item['level']
        url = item['url']
        
        # 移除超出当前级别的栈元素
        while stack and stack[-1]['level'] >= level:
            stack.pop()
        
        # 创建当前节点
        node = {
            'title': title,
            'url': url,
            'children': []
        }
        
        # 添加到父节点或根节点
        if stack:
            stack[-1]['children'].append(node)
        else:
            tree.append(node)
        
        # 将当前节点加入栈
        stack.append(node)
    
    return tree

def generate_html_tree(tree):
    """生成HTML格式的目录树"""
    def _generate_node(node, level):
        indent = '  ' * level
        if node['url']:
            return f'{indent}<li class="chm-tree-item" data-url="{node["url"]}">{node["title"]}</li>\n' + ''.join(_generate_node(child, level + 1) for child in node['children'])
        else:
            return f'{indent}<li class="chm-tree-item parent">{node["title"]}</li>\n' + ''.join(_generate_node(child, level + 1) for child in node['children'])
    
    html = '<ul class="chm-tree">\n'
    for node in tree:
        html += _generate_node(node, 0)
    html += '</ul>'
    
    return html

if __name__ == '__main__':
    wcp_file = '天舟.wcp'
    titles = parse_wcp_file(wcp_file)
    tree = build_tree(titles)
    html_tree = generate_html_tree(tree)
    
    # 保存到文件
    with open('toc.html', 'w', encoding='utf-8') as f:
        f.write(html_tree)
    
    print("目录树已保存到toc.html文件")
