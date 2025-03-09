#!/usr/bin/env python3
import sys
import xmltodict
import pandas as pd


def parse_xml(filename: str) -> dict[str, str]:
    with open(filename) as f:
        return xmltodict.parse(f.read())

def write_excel(data: list, filename: str) -> None:
    df = pd.DataFrame('', index = range(100), columns = range(100))
    for path in data:
        df.iloc[int(path['from']), int(path['to'])] = int(path['read'])
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
