#!/usr/bin/env python3
import sys
import xmltodict
import pandas as pd


def parse_xml(filename: str) -> dict[str, str]:
    with open(filename) as f:
        return xmltodict.parse(f.read())

def write_excel(data: list, filename: str) -> None:
    rows = {f'q{path['from']}' for path in data}
    cols = {f'q{path['to']}' for path in data}
    df = pd.DataFrame(index=sorted(rows), columns=sorted(cols))
    for path in data:
        df.at[f'q{path["from"]}', f'q{path["to"]}'] = path["read"]
    df = df[sorted(df.columns, key=lambda x: int(x[1:]))]
    df = df.reindex(sorted(df.index, key=lambda x: int(x[1:])))
    df.to_excel(filename)

def main():
    print("Starting...")
    filename = sys.argv[1]
    new_file = sys.argv[2]
    print(f"Reading file {filename}")
    schema = parse_xml(filename)["structure"]["automaton"]['transition']
    for transition in schema:
        print(transition)
    write_excel(schema, new_file)
    print("Done")


if __name__ == '__main__':
    main()
