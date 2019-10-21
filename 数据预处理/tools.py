import pandas as pd
import numpy as np
import time

# 读取CSV
def read_csv(csv_path):
    return pd.read_csv(csv_path, header=0)

# 保存CSV
def save_csv(csv_path, filename, table):
    table.to_csv(csv_path + filename, index=False, sep=',', header=1, encoding='utf_8_sig')

# 处理account表中非int类型数据
def account_process_not_int(x):
        try:
            x = int(x)
            return x
        except:
            x = str(x)
            return int(x[0:4])

# 判断是否为int
def is_int(x):
    return not not_int(x)

def not_int(x):
    try:
        x = int(x)
        return False
    except:
        return True

# 判断日期
def not_date(x, format):
    try:
        time.strptime(x, format)
        return False
    except:
        return True

# 判断日期是否合法
def is_birth_legal(birth_number):
    birth_number = str(birth_number)
    year = 1900 + int(birth_number[0:2])
    try:
        month = int(birth_number[2:4])
    except:
        return False
    day = int(birth_number[4:6])

    if month > 12:
        month -= 50
        if month <= 0:
            return False

    try:
        time.strptime(str(year) + '-' + str(month) + '-' + str(day), "%Y-%m-%d")
        return True
    except:
        return False

# 处理card表中根据birth分男女
def card_process_birth(birth_number):
    birth_number = str(birth_number)
    year = 1900 + int(birth_number[0:2])
    month = int(birth_number[2:4])
    day = int(birth_number[4:6])
    if month > 12:
        sex = 'Female'
        month -= 50
    else:
        sex = 'Male'
    birth_day = pd.datetime(year=year, month=month, day=day)

    return pd.Series([birth_day, sex])

# 处理loan表中duration
# duration应为12的倍数, 否则置位NAN
def loan_process_duration(x):
    x = int(x)
    if x < 0:
        return np.NaN
    if x % 12 == 0:
        return x
    else:
        return np.NaN

# 处理loan表中payment
# payment * duration = Amount
def loan_process_payment(payment, duration, amount):
    if payment * duration == amount:
        return True
    else:
        return False

# 判断外键关联
# 判断table中是否存在该id
def is_exist(x, table, id_name):
    if table[(table[id_name] == x)].empty:
        return False
    else:
        return True