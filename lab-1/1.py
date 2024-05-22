import re
import pandas as pd
import copy
import numpy as np


def parse_line(line: str) -> dict | None:
    regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes_sent>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    match = re.match(regex, line)
    return match.groupdict() if match else None


def parse_file(filepath: str) -> pd.DataFrame:

    with open(filepath, 'r') as file:
        df_rows = []
        for line in file:
            row = parse_line(line)
            # print(row)
            if not(row is None):
                df_rows.append(row)
        
    df = pd.DataFrame(df_rows)
    # етап обробки датафрейму
    # df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df['status'] = pd.to_numeric(df['status'], errors='coerce')
    df['bytes_sent'] = pd.to_numeric(df['bytes_sent'], errors='coerce')
    df['date'] = df['timestamp'].dt.date
    df['endpoint'] = df['request'].apply(lambda x: x.split()[1])
    return copy.deepcopy(df)


def main():

    # ======= task a
    filepath = 'lab-1/access.log'
    df = parse_file(filepath)
    df.to_csv('lab-1/access_log.csv')
    print(df.head())

    # ======= task b

    # ======= task c

    # ======= task d

    # ======= task e


if __name__ == '__main__':
    main()



