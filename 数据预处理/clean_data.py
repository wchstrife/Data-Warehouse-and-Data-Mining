import pandas as pd
import numpy as np

import time
import os

import tools

CLEAN_DATA_PATH = './clean_data/'    # 处理后数据路径

# 处理account表
def process_account():
    account = tools.read_csv('./dirty_data/account.csv')

    account.drop_duplicates(inplace=True)                                                   # 去重  
    account['frequency'].replace({"POPLATEKMESICNE": "POPLATEK MESICNE"}, inplace=True)     # frequency : POPLATEKMESICNE -> POPLATEK MESICNE

    # 转换数据类型
    account['account_id'] = account['account_id'].apply(tools.account_process_not_int)              
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

# 处理disp表
def process_disp():
    disp = tools.read_csv('./dirty_data/disp.csv')

    disp.drop_duplicates(inplace=True)    

    return disp

# 处理district表
def process_district():
    district = tools.read_csv('./dirty_data/district.csv')

    district.drop_duplicates(inplace=True)    
    
    return district

# 处理loan表
def process_loan():
    loan = tools.read_csv('./dirty_data/loan.csv')

    loan['duration'] = loan['duration'].apply(tools.loan_process_duration)     # 处理duration为整12倍数
    loan = loan[loan['duration'].notnull()]
    loan = loan[loan.apply(lambda row: tools.loan_process_payment(row['payments'], row['duration'], row['amount']), axis=1)]    # 处理 payment * duration = amount

    return loan

# 处理order表
def process_order():
    order = tools.read_csv('./dirty_data/order.csv')

    order.drop_duplicates(inplace=True)  

    return order 

# 处理trans表
def process_trans():
    trans = tools.read_csv('./dirty_data/trans.csv')

    trans = trans[trans['balance'].apply(tools.is_int)]     # 处理balance非int
    trans['balance'] = pd.to_numeric(trans['balance'])
    trans = trans[trans['bank'].notnull()]                  # 处理bank有空值
    trans['date'] = pd.to_datetime(trans['date'])           # 格式化date

    return trans


if __name__ == "__main__":
    
    # 读取csv
    account = process_account()
    card = process_card()
    client = process_client()
    disp = process_disp()
    district = process_district()
    loan = process_loan()
    order = process_order()
    trans = process_trans()

    # 每一次对表中的外键进行检查
    # 保存到clean_data目录下
    account = account[account['district_id'].apply(lambda x: tools.is_exist(x, district, 'district_id'))]  
    tools.save_csv(CLEAN_DATA_PATH, 'account.csv', account)

    card = card[card['disp_id'].apply(lambda x: tools.is_exist(x, disp, 'disp_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'card.csv', card)

    client = client[client['district_id'].apply(lambda x: tools.is_exist(x, district, 'district_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'client.csv', client)

    disp = disp[disp['client_id'].apply(lambda x: tools.is_exist(x, client, 'client_id'))]
    disp = disp[disp['account_id'].apply(lambda x: tools.is_exist(x, account, 'account_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'disp.csv', disp)

    tools.save_csv(CLEAN_DATA_PATH, 'district.csv', district)

    loan = loan[loan['account_id'].apply(lambda x: tools.is_exist(x, account, 'account_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'loan.csv', loan)

    order = order[order['account_id'].apply(lambda x: tools.is_exist(x, account, 'account_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'order.csv', order)

    trans = trans[trans['account_id'].apply(lambda x: tools.is_exist(x, account, 'account_id'))]
    tools.save_csv(CLEAN_DATA_PATH, 'trans.csv', trans)


    
    