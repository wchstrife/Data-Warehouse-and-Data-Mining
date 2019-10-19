import pandas as pd
import numpy as np

# 读取CSV
def read_csv(csv_path):
    return pd.read_csv(csv_path, header=0)

# 处理account表中非int类型数据
def process_not_int(x):
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

# 判断日期是否非法
def is_birth_legal(birth_number):
    return not is_birth_illegal(birth_number)

def is_birth_illegal(birth_number):
    birth_number = str(birth_number)
    year = 1900 + int(birth_number[0:2])
    try:
        month = int(birth_number[2:4])
    except:
        return True
    day = int(birth_number[4:6])

    if month > 12:
        month -= 50
        if month <= 0:
            return True

    try:
        time.strptime(str(year) + '-' + str(month) + '-' + str(day), "%Y-%m-%d")
        return False
    except:
        return True

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