import pandas as pd
import numpy as np

import time
import os

import shutil
import tools

DIRTY_DATA_PATH = './dirty_data'      # 处理前数据路径
CLEAN_DATA_PATH = './clean_data'    # 处理后数据路径

# 处理account表
def process_account():
    account = tools.read_csv('./dirty_data/account.csv')

    account.drop_duplicates(inplace=True)                                                   # 去重  
    account['frequency'].replace({"POPLATEKMESICNE": "POPLATEK MESICNE"}, inplace=True)     # frequency : POPLATEKMESICNE -> POPLATEK MESICNE

    # 转换数据类型
    account['account_id'] = account['account_id'].apply(tools.process_not_int)              
    account['date'] = pd.to_datetime(account['date'])
    
    return account

# 处理card表
def process_card():
    card = tools.read_csv('./dirty_data/card.csv')

    card['type'].replace({"golden": "gold"}, inplace=True)          # type : golden -> gold
    card['issued'] = pd.to_datetime(card['issued'])

    return card

# 处理client表
def process_client():
    client = tools.read_csv('./dirty_data/client.csv')

    client = client[client['birth_number'].apply(tools.is_birth_legal)]
    client[['birth_day', 'gender']] = client['birth_number'].apply(tools.card_process_birth)  # 根据出生日期分男女
    client.drop(columns=['birth_number'], inplace=True)

    return client

if __name__ == "__main__":
    temp = process_client()
    print(temp.dtypes)