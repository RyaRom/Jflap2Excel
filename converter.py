#!/usr/bin/env python3
import sys
import xmltodict
import pandas as pd


def parse_xml(filename: str) -> dict[str, str]:
    with open(filename) as f:
        return xmltodict.parse(f.read())


def write_fa(data, filename: str) -> None:
    rows = {path['read'] for path in data}
    cols = {f'q{path['from']}' for path in data}
    df = pd.DataFrame(index=sorted(rows), columns=sorted(cols))
    for path in data:
        df.at[path["read"], f'q{path["from"]}'] = f'q{path["to"]}'
    df = df[sorted(df.columns, key=lambda x: int(x[1:]))]
    df.to_excel(filename)


def write_mealy(data, filename: str) -> None:
    rows = {path['read'] for path in data}
    cols = {f'a{path['from']}' for path in data}
    df = pd.DataFrame(index=sorted(rows), columns=sorted(cols))
    for path in data:
        df.at[path["read"], f'a{path["from"]}'] = f'a{path["to"]}/{path['transout']}'
    df = df[sorted(df.columns, key=lambda x: int(x[1:]))]
    df.to_excel(filename)


def write_moore(data, filename: str) -> None:
    rows = {path['read'] for path in data}
    cols = {f'a{path['from']}' for path in data}
    df = pd.DataFrame(index=sorted(rows), columns=sorted(cols))
    for path in data:
        df.at["out", f'a{path["to"]}'] = path["transout"]
        df.at[path["read"], f'a{path["from"]}'] = f'a{path["to"]}'
    df = df[sorted(df.columns, key=lambda x: int(x[1:]))]
    df.to_excel(filename)


def main():
    print("Starting...")
    filename = sys.argv[1]
    new_file = sys.argv[2]
    print(f"Reading file {filename}")
    structure = parse_xml(filename)["structure"]
    schema = structure["automaton"]['transition']
    automata_type = structure["type"]
    print(f'Type = \"{automata_type}\"')
    for transition in schema:
        print(transition)
    match automata_type:
        case "fa":
            write_fa(schema, new_file)
        case "mealy":
            write_mealy(schema, new_file)
        case "moore":
            write_moore(schema, new_file)
        case _:
            raise ValueError(f"Unknown automata type {automata_type}")
    print("Done")


if __name__ == '__main__':
    main()
