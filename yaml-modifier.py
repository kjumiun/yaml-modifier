# -*- coding: utf-8 -*-
import sys
from ruamel.yaml import YAML
import argparse

def modify_yaml(input_file, output_file, modifications):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(input_file, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

    for key, value in modifications:
        keys = key.split('.')
        current = data
        for k in keys[:-1]:
            if k.isdigit():
                k = int(k)
            if isinstance(current, list) and isinstance(k, int) and 0 <= k < len(current):
                current = current[k]
            elif isinstance(current, dict) and k in current:
                current = current[k]
            else:
                print(f"警告: キー '{k}' がYAMLファイルに見つかりません。")
                break
        else:
            last_key = keys[-1]
            if last_key.isdigit():
                last_key = int(last_key)
            if isinstance(current, list) and isinstance(last_key, int) and 0 <= last_key < len(current):
                current[last_key] = value
            elif isinstance(current, dict) and last_key in current:
                current[last_key] = value
            else:
                print(f"警告: キー '{last_key}' がYAMLファイルに見つかりません。")

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)


def main():
    parser = argparse.ArgumentParser(description="YAMLファイルの値を修正します")
    parser.add_argument("input_file", nargs='?', help="入力YAMLファイルのパス")
    parser.add_argument("-m", "--modify", nargs=2, action='append', metavar=('キー', '値'),
                        help="修正するキーと新しい値（複数回使用可能）")
    parser.add_argument("-o", "--output", help="出力YAMLファイルのパス（デフォルト: 入力ファイルと同じ）")
    
    args = parser.parse_args()

    if not args.input_file or not args.modify:
        parser.print_help()
        sys.exit(1)

    output_file = args.output if args.output else args.input_file

    modify_yaml(args.input_file, output_file, args.modify)
    print(f"YAMLファイルが修正され、{output_file}に保存されました。")

if __name__ == "__main__":
    main()
