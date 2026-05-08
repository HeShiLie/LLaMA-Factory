#!/usr/bin/env python3
"""
修复 LlamaFactory 的 StrEnum 兼容性问题
使其可以在 Python 3.10 环境下运行
"""
import re
import os

# 定义要修改的文件列表
files = [
    "src/llamafactory/extras/constants.py",
    "src/llamafactory/data/data_utils.py",
    "src/llamafactory/v1/accelerator/helper.py",
    "src/llamafactory/v1/accelerator/interface.py",
    "src/llamafactory/v1/config/arg_utils.py",
    "src/llamafactory/api/protocol.py"
]

# 定义替换模式
pattern1 = r'from enum import StrEnum, unique'
replacement1 = '''import sys
from enum import unique

# Python 3.11+ 才有 StrEnum，3.10 需要自己实现
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum
    class StrEnum(str, Enum):
        """StrEnum for Python < 3.11"""
        pass'''

pattern2 = r'^from enum import StrEnum$'
replacement2 = '''import sys
from enum import Enum

# Python 3.11+ 才有 StrEnum，3.10 需要自己实现
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    class StrEnum(str, Enum):
        """StrEnum for Python < 3.11"""
        pass'''

def main():
    success_count = 0
    fail_count = 0
    
    print("开始修复 StrEnum 兼容性问题...\n")
    
    # 处理每个文件
    for file_path in files:
        if os.path.exists(file_path):
            print(f"处理 {file_path}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 先尝试替换 "from enum import StrEnum, unique"
                if 'from enum import StrEnum, unique' in content:
                    content = re.sub(pattern1, replacement1, content)
                    print(f"  ✓ 已替换 'from enum import StrEnum, unique'")
                # 再尝试替换单独的 "from enum import StrEnum"
                elif re.search(pattern2, content, re.MULTILINE):
                    content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)
                    print(f"  ✓ 已替换 'from enum import StrEnum'")
                else:
                    print(f"  ⚠ 未找到 StrEnum 导入")
                    continue
                
                # 只有内容真的改变了才写入
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✓ {file_path} 处理成功")
                    success_count += 1
                else:
                    print(f"  ⚠ {file_path} 无需修改")
                    
            except Exception as e:
                print(f"  ✗ 处理 {file_path} 时出错: {e}")
                fail_count += 1
        else:
            print(f"  ✗ {file_path} 文件不存在")
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"修复完成！")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
