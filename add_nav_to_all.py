#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为所有HTML文件添加导航

此脚本用于遍历项目中的所有HTML文件，并在每个文件中添加对nav.js的引用，
以便在所有页面中显示导航栏。
"""

import os
import re

def add_nav_to_html(file_path, nav_js_path='nav.js'):
    """
    为单个HTML文件添加导航
    
    Args:
        file_path: HTML文件路径
        nav_js_path: nav.js文件的相对路径
    """
    try:
        # 读取HTML文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加了nav.js引用
        if f'<script src="{nav_js_path}">' in content:
            print(f"{file_path} 已经添加了导航引用，跳过")
            return False
        
        # 查找</head>标签并在其前添加script标签
        head_end_pattern = r'</head>'
        if re.search(head_end_pattern, content):
            # 在</head>前添加script标签
            new_content = re.sub(head_end_pattern, f'<script src="{nav_js_path}"></script>\n</head>', content)
        else:
            # 如果没有</head>标签，在<body>前添加
            body_start_pattern = r'<body>'
            if re.search(body_start_pattern, content):
                new_content = re.sub(body_start_pattern, f'<head>\n<script src="{nav_js_path}"></script>\n</head>\n<body>', content)
            else:
                # 如果连<body>标签都没有，在文件开头添加
                new_content = f'<html>\n<head>\n<script src="{nav_js_path}"></script>\n</head>\n<body>\n' + content + '\n</body>\n</html>'
        
        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"成功为 {file_path} 添加了导航引用")
        return True
    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")
        return False

def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='批量为所有HTML文件添加导航')
    parser.add_argument('--root', '-r', default='.', help='根目录路径')
    parser.add_argument('--nav-js', default='nav.js', help='nav.js文件的相对路径')
    
    args = parser.parse_args()
    
    try:
        root_dir = args.root
        nav_js_path = args.nav_js
        
        print(f"开始为目录 {root_dir} 中的所有HTML文件添加导航...")
        print(f"使用的nav.js路径: {nav_js_path}")
        
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        # 遍历目录
        for root, dirs, files in os.walk(root_dir):
            # 跳过.files目录
            if '.files' in root:
                continue
            
            for file in files:
                if file.endswith('.html') or file.endswith('.htm'):
                    # 跳过nav.html本身
                    if file == 'nav.html':
                        skipped_count += 1
                        continue
                    
                    file_path = os.path.join(root, file)
                    print(f"处理文件: {file_path}")
                    
                    # 计算nav.js的相对路径
                    rel_path = os.path.relpath(os.path.dirname(file_path), root_dir)
                    if rel_path == '.':
                        current_nav_js_path = nav_js_path
                    else:
                        # 向上返回的路径
                        up_path = '../' * len(rel_path.split(os.sep))
                        current_nav_js_path = up_path + nav_js_path
                    
                    print(f"  使用nav.js路径: {current_nav_js_path}")
                    
                    # 添加导航
                    result = add_nav_to_html(file_path, current_nav_js_path)
                    if result:
                        processed_count += 1
                    else:
                        skipped_count += 1
        
        print(f"\n处理完成！")
        print(f"成功处理: {processed_count} 个文件")
        print(f"跳过: {skipped_count} 个文件")
        print(f"错误: {error_count} 个文件")
        
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
