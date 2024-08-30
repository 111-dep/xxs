import json
import click
"""
执行命令 python reformat_json.py input.json --max-length 220

"""

def reformat_json(file_path, max_length):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def format_json(obj, level=0):
        indent = ' ' * 4 * level  # 计算当前缩进
        if isinstance(obj, dict):
            items = []
            for k, v in obj.items():
                formatted_value = format_json(v, level + 1)  # 递归格式化值
                item = f'"{k}": {formatted_value}'
                items.append(item)
            if len(items) == 0:
                return '{}'
            single_line = f'{{ {", ".join(items)} }}'
            # 如果单行长度小于最大长度，则合并成一行
            if len(single_line) + len(indent) < max_length:
                return single_line
            else:
                # 否则分多行显示
                return f'{{\n{indent}    ' + f',\n{indent}    '.join(items) + f'\n{indent}}}'
        elif isinstance(obj, list):
            items = [format_json(i, level + 1) for i in obj]  # 递归格式化列表项
            if len(items) == 0:
                return '[]'
            single_line = f'[ {", ".join(items)} ]'
            # 如果单行长度小于最大长度，则合并成一行
            if len(single_line) + len(indent) < max_length:
                return single_line
            else:
                # 否则分多行显示
                return f'[\n{indent}    ' + f',\n{indent}    '.join(items) + f'\n{indent}]'
        else:
            # 处理基本类型，确保 Unicode 字符正确显示
            return json.dumps(obj, ensure_ascii=False)

    formatted_json = format_json(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_json)


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--max-length', default=220, help='Maximum length of a line.')
def main(file_path, max_length):
    """Reformat JSON file to merge short lines and keep long lines."""
    reformat_json(file_path, max_length)


if __name__ == '__main__':
    main()