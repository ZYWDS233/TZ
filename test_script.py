print("Hello, World!")
print("Testing Python script execution...")

# 测试文件操作
with open('test_output.txt', 'w') as f:
    f.write('Test output')
print("File write test completed.")

# 测试目录遍历
import os
print("Current directory:", os.getcwd())
print("Files in current directory:")
for file in os.listdir('.'):
    if os.path.isfile(file):
        print(f"  - {file}")
