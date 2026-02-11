#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 简单的测试脚本，用于验证WCP文件读取

print("开始测试...")
try:
    with open('天舟.wcp', 'r', encoding='utf-8') as f:
        content = f.read()
        print("文件读取成功！")
        print(f"文件大小：{len(content)} 字节")
        
        # 打印文件开头部分
        print("\n文件开头部分：")
        print(content[:1000])
    print("测试完成！")
except Exception as e:
    print(f"错误：{e}")
