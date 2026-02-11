import os

def add_nav_to_file(file_path, nav_js_path):
    """
    为单个HTML文件添加nav.js引用
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加了nav.js引用
        if f'<script src="{nav_js_path}">' in content:
            print(f"跳过: {file_path} (已添加)")
            return False
        
        # 查找</head>标签
        head_end_pos = content.find('</head>')
        if head_end_pos != -1:
            # 在</head>前添加script标签
            new_content = content[:head_end_pos] + f'<script src="{nav_js_path}"></script>' + content[head_end_pos:]
            
            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"成功: {file_path}")
            return True
        else:
            print(f"跳过: {file_path} (无</head>标签)")
            return False
    except Exception as e:
        print(f"错误: {file_path} - {e}")
        return False

def main():
    """
    主函数
    """
    root_dir = '.'
    processed = 0
    skipped = 0
    errors = 0
    
    print("开始批量添加导航引用...")
    
    # 遍历所有文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过.files目录
        if '.files' in root:
            continue
        
        for file in files:
            if file.endswith('.html') or file.endswith('.htm'):
                # 跳过nav.html
                if file == 'nav.html':
                    skipped += 1
                    continue
                
                file_path = os.path.join(root, file)
                
                # 计算nav.js的相对路径
                rel_path = os.path.relpath(os.path.dirname(file_path), root_dir)
                if rel_path == '.':
                    nav_js_path = 'nav.js'
                else:
                    # 向上返回的路径
                    up_levels = rel_path.count(os.sep) + 1
                    nav_js_path = '../' * up_levels + 'nav.js'
                
                # 添加导航引用
                result = add_nav_to_file(file_path, nav_js_path)
                if result:
                    processed += 1
                else:
                    skipped += 1
    
    print(f"\n处理完成!")
    print(f"成功处理: {processed} 个文件")
    print(f"跳过: {skipped} 个文件")
    print(f"错误: {errors} 个文件")

if __name__ == '__main__':
    main()
