#!/usr/bin/env python3
"""
修复 LlamaFactory 的 NotRequired 兼容性问题
使其可以在 Python 3.10 环境下运行
"""
import os

files = [
    "src/llamafactory/data/template.py",
    "src/llamafactory/data/mm_plugin.py"
]

def fix_file(file_path):
    if not os.path.exists(file_path):
        print(f"✗ {file_path} 不存在")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'NotRequired' not in content:
        print(f"⚠ {file_path} 不包含 NotRequired")
        return False
    
    lines = content.split('\n')
    new_lines = []
    replaced = False
    
    for line in lines:
        if 'from typing import' in line and 'NotRequired' in line:
            if not replaced:
                imports = line.replace('from typing import', '').strip()
                imports_list = [x.strip() for x in imports.split(',')]
                other_imports = [x for x in imports_list if x != 'NotRequired']
                
                new_lines.append('import sys')
                new_lines.append(f'from typing import {", ".join(other_imports)}')
                new_lines.append('')
                new_lines.append('# Python 3.11+ 才有 NotRequired，3.10 需要从 typing_extensions 导入')
                new_lines.append('if sys.version_info >= (3, 11):')
                new_lines.append('    from typing import NotRequired')
                new_lines.append('else:')
                new_lines.append('    from typing_extensions import NotRequired')
                replaced = True
        else:
            new_lines.append(line)
    
    if replaced:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"✓ {file_path} 修复成功")
        return True
    return False

def main():
    print("开始修复 NotRequired 兼容性问题...\n")
    success = sum(fix_file(f) for f in files)
    print(f"\n{'='*60}")
    print(f"修复完成！成功修复 {success}/{len(files)} 个文件")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
