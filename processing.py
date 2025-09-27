#!/usr/bin/env python3

import argparse
import pandas as pd
from pathlib import Path
import re


def parse_copy_postgres(sql_file: str, output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(sql_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.upper().startswith('COPY'):
            m = re.match(r'COPY (?:"?[a-zA-Z0-9_]+"?\.)?"?([a-zA-Z0-9_]+)"? \((.*?)\) FROM stdin;', line, re.IGNORECASE)
            if m:
                table_name = m.group(1)
                columns = [c.strip() for c in m.group(2).split(',')]
                i += 1
                data_rows = []
                while i < len(lines) and lines[i].strip() != '\\.' and lines[i].strip() != '\.':
                    row = lines[i].rstrip('\n').split('\t')
                    data_rows.append(row)
                    i += 1
                if data_rows:
                    df = pd.DataFrame(data_rows, columns=columns)
                    df.to_csv(output_dir / f"{table_name}.csv", index=False)
                    print(f"Сохранил таблицу {table_name}, строк: {len(df)}")
                else:
                    print(f"Нет данных для таблицы {table_name}")
        i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql-file', required=True)
    parser.add_argument('--output-dir', default='./dataset_raw')
    args = parser.parse_args()
    print('Обрабатываем дамп и сохраняем таблицы в CSV...')
    parse_copy_postgres(args.sql_file, args.output_dir)
    print('Готово. CSV по таблицам сохранены в папке', args.output_dir)

if __name__ == '__main__':
    main()