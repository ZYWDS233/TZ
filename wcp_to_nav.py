#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WCP文件转换为网页导航工具

此脚本用于解析WinCHM项目文件（.wcp）中的目录结构，并生成一个HTML导航文件。
生成的导航文件可以直接嵌入到网页中，提供类似CHM文件的导航功能。
"""

import re
import os


def parse_wcp_file(wcp_path):
    """
    解析WCP文件，提取目录结构
    
    Args:
        wcp_path: WCP文件路径
    
    Returns:
        目录项列表，每个目录项包含title、level和url
    """
    with open(wcp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取TitleList部分
    topics_section = re.search(r'\[TOPICS\](.*?)(?=\[|$)', content, re.DOTALL)
    if not topics_section:
        raise ValueError("未找到[TOPICS]部分")
    
    topics_content = topics_section.group(1)
    
    # 提取标题数量
    title_count_match = re.search(r'TitleList=(\d+)', topics_content)
    if not title_count_match:
        raise ValueError("未找到TitleList数量")
    
    title_count = int(title_count_match.group(1))
    
    # 提取每个标题的信息
    items = []
    for i in range(title_count):
        title_match = re.search(rf'TitleList\.Title\.{i}=(.*?)\n', topics_content)
        level_match = re.search(rf'TitleList\.Level\.{i}=(\d+)\n', topics_content)
        url_match = re.search(rf'TitleList\.Url\.{i}=(.*?)\n', topics_content)
        
        if title_match and level_match:
            title = title_match.group(1)
            level = int(level_match.group(1))
            url = url_match.group(1) if url_match else ''
            
            # 跳过没有URL的项
            if url:
                items.append({
                    'title': title,
                    'level': level,
                    'url': url
                })
    
    return items


def generate_nav_html(items, output_path='nav.html', site_title='网站导航'):
    """
    根据目录项列表生成HTML导航文件
    
    Args:
        items: 目录项列表
        output_path: 输出HTML文件路径
        site_title: 网站标题
    """
    # 生成导航HTML
    nav_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="gb2312">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <style>
        /* 导航栏样式 */
        .sidebar {
            width: 270px;
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            background: #f0f0f0;
            padding: 20px;
            overflow-y: auto;
            font-family: Arial, DengXian, Microsoft YaHei, sans-serif;
        }
        
        .sidebar h3 {
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }
        
        .sidebar ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        
        .sidebar ul ul {
            padding-left: 20px;
        }
        
        .sidebar li {
            margin: 5px 0;
        }
        
        .sidebar a {
            color: #333;
            text-decoration: none;
            display: block;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .sidebar a:hover {
            background-color: #e0e0e0;
        }
        
        /* 内容区域样式 */
        .content {
            margin-left: 290px;
            padding: 20px;
            font-family: Arial, DengXian, Microsoft YaHei, sans-serif;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
                max-height: 300px;
            }
            .content {
                margin-left: 0;
            }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>{site_title}</h3>
        <ul>
    """
    
    # 生成导航列表
    current_level = 0
    for item in items:
        level = item['level']
        title = item['title']
        url = item['url']
        
        # 处理层级变化
        if level > current_level:
            # 增加缩进
            nav_html += ' ' * (current_level * 4) + '<ul>\n'
        elif level < current_level:
            # 减少缩进
            nav_html += ' ' * (level * 4) + '</ul>\n' * (current_level - level)
        
        # 添加导航项
        nav_html += f"{' ' * (level * 4)}<li><a href=\"{url}\" target=\"_top\">{title}</a></li>\n"
        
        current_level = level
    
    # 关闭所有未关闭的ul标签
    if current_level > 0:
        nav_html += ' ' * ((current_level - 1) * 4) + '</ul>\n' * current_level
    
    # 结束HTML
    nav_html += f"""
        </ul>
    </div>
    <div class="content">
        <h1>欢迎访问网站</h1>
        <p>请使用左侧导航栏浏览内容。</p>
    </div>
</body>
</html>
    """
    
    # 写入文件
    with open(output_path, 'w', encoding='gb2312') as f:
        f.write(nav_html)
    
    print(f"导航文件已生成：{output_path}")


def generate_nav_js(items, output_path='nav.js'):
    """
    生成导航JavaScript文件，用于在其他页面中加载导航
    
    Args:
        items: 目录项列表
        output_path: 输出JavaScript文件路径
    """
    # 生成导航HTML字符串
    nav_html = '<h3>网站导航</h3><ul>\n'
    
    current_level = 0
    for item in items:
        level = item['level']
        title = item['title']
        url = item['url']
        
        # 处理层级变化
        if level > current_level:
            # 增加缩进
            nav_html += ' ' * (current_level * 4) + '<ul>\n'
        elif level < current_level:
            # 减少缩进
            nav_html += ' ' * (level * 4) + '</ul>\n' * (current_level - level)
        
        # 添加导航项
        nav_html += f"{' ' * (level * 4)}<li><a href=\"{url}\" target=\"_top\">{title}</a></li>\n"
        
        current_level = level
    
    # 关闭所有未关闭的ul标签
    if current_level > 0:
        nav_html += ' ' * ((current_level - 1) * 4) + '</ul>\n' * current_level
    
    nav_html += '</ul>'
    
    # 生成JavaScript文件
    js_content = f"""
// 导航栏HTML
const navHtml = `{nav_html}`;

// 加载导航栏
function loadNavigation() {
    // 创建导航栏容器
    const navContainer = document.createElement('div');
    navContainer.className = 'sidebar';
    navContainer.innerHTML = navHtml;
    
    // 将导航栏添加到页面顶部
    document.body.insertAdjacentElement('afterbegin', navContainer);
    
    // 调整内容区域位置
    document.body.style.margin = '0';
    
    // 创建内容容器
    const contentContainer = document.createElement('div');
    contentContainer.className = 'content';
    
    // 移动现有内容到内容容器
    while (document.body.children.length > 1) {
        if (document.body.children[1].className !== 'sidebar') {
            contentContainer.appendChild(document.body.children[1]);
        } else {
            break;
        }
    }
    
    // 添加内容容器到页面
    document.body.appendChild(contentContainer);
}

// 页面加载完成后加载导航栏
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavigation);
} else {
    loadNavigation();
}
    """
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"导航JavaScript文件已生成：{output_path}")


def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='WCP文件转换为网页导航工具')
    parser.add_argument('wcp_file', help='WCP文件路径')
    parser.add_argument('--output', '-o', default='nav.html', help='输出HTML文件路径')
    parser.add_argument('--title', '-t', default='网站导航', help='网站标题')
    parser.add_argument('--js', action='store_true', help='同时生成JavaScript文件')
    
    args = parser.parse_args()
    
    try:
        # 检查WCP文件是否存在
        if not os.path.exists(args.wcp_file):
            print(f"错误：WCP文件 {args.wcp_file} 不存在")
            return
        
        # 解析WCP文件
        print(f"正在解析WCP文件：{args.wcp_file}")
        items = parse_wcp_file(args.wcp_file)
        print(f"成功解析 {len(items)} 个导航项")
        
        # 生成HTML导航文件
        generate_nav_html(items, args.output, args.title)
        print(f"导航HTML文件已生成：{os.path.abspath(args.output)}")
        
        # 生成JavaScript文件（如果需要）
        if args.js:
            js_output = os.path.splitext(args.output)[0] + '.js'
            generate_nav_js(items, js_output)
            print(f"导航JavaScript文件已生成：{os.path.abspath(js_output)}")
            
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
