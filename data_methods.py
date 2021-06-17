import csv
from csv import DictReader
import os
from threading import Thread

already_working = 0
result = 0


def get_all_data():
    base = []
    with open("data.csv", mode="r", encoding="utf-8", newline="") as file:
        for row in DictReader(file):
            base.append(row)
    return base


def get_info_by_user_id_and_(user_id, nickname=None, password=None, number=None):
    global result
    base = get_all_data()
    if user_id and nickname and password:
        for base_element in base:
            if user_id == base_element['user_id'] and nickname == base_element['nickname'] and \
                    password == base_element['password']:
                result = base_element
                return
    elif user_id and nickname:
        for base_element in base:
            if user_id == base_element['user_id'] and nickname == base_element['nickname']:
                result = base_element
                return
    elif user_id:
        for base_element in base:
            if user_id == base_element['user_id']:
                result = base_element
                return

    result = 0


def edit_info_by_(mode=None, user_id=None, nickname=None, password=None, cash=None, txnId=None):
    global result
    if mode == 'add_auth':
        input_file = open('data.csv', 'r')
        output_file = open('data1.csv', 'w')
        writer = csv.writer(output_file)
        for row in csv.reader(input_file):
            if row[0] != user_id:
                writer.writerow(row)
            else:
                writer.writerow([row[tmp] for tmp in range(4)] + ['2'] + [row[tmp] for tmp in range(5, 8)])
        input_file.close()
        output_file.close()
        os.rename('data.csv', 'temp.csv')
        os.rename('data1.csv', 'data.csv')
        os.rename('temp.csv', 'data1.csv')
        result = 1
    elif mode == 'add_reg':
        file = open('data.csv', 'a')
        writer = csv.writer(file)
        writer.writerow([user_id, nickname, password, '0', '1'] + ['0' for tmp in range(4)])
        file.close()
        result = 1
    elif mode == 'del':
        input_file = open('data.csv', 'r')
        output_file = open('data1.csv', 'w')
        writer = csv.writer(output_file)
        for row in csv.reader(input_file):
            if row[0] != user_id:
                writer.writerow(row)
        input_file.close()
        output_file.close()
        os.rename('data.csv', 'temp.csv')
        os.rename('data1.csv', 'data.csv')
        os.rename('temp.csv', 'data1.csv')
        result = 1
    elif mode == 'minus_cash':
        input_file = open('data.csv', 'r')
        output_file = open('data1.csv', 'w')
        writer = csv.writer(output_file)
        for row in csv.reader(input_file):
            if row[0] != user_id:
                writer.writerow(row)
            else:
                writer.writerow([row[tmp] for tmp in range(6)] + [str(float(row[6]) - float(cash))] + [row[7]])
        input_file.close()
        output_file.close()
        os.rename('data.csv', 'temp.csv')
        os.rename('data1.csv', 'data.csv')
        os.rename('temp.csv', 'data1.csv')
        result = 1
    elif mode == 'plus_cash_txnId':
        input_file = open('data.csv', 'r')
        output_file = open('data1.csv', 'w')
        writer = csv.writer(output_file)
        for row in csv.reader(input_file):
            if row[0] != user_id:
                writer.writerow(row)
            else:
                writer.writerow([row[tmp] for tmp in range(6)] + [str(float(row[6]) + float(cash))] + [txnId])
        input_file.close()
        output_file.close()
        os.rename('data.csv', 'temp.csv')
        os.rename('data1.csv', 'data.csv')
        os.rename('temp.csv', 'data1.csv')
        result = 1


def find_in_friends(user_id=None):
    global result
    get_info_by_user_id_and_(user_id=user_id)
    file = open('fi_friends')
    nicknames = file.read().split()
    for nickname in nicknames:
        if nickname == result['nickname']:
            edit_info_by_(mode='add_auth',
                          user_id=user_id)
            result = 1
            return
    result = 0


def start_method(name, user_id=None, nickname=None, password=None, cash=None, txnId=None):
    user_id = str(user_id)
    cash = str(cash)
    global already_working, result
    if already_working:
        print('[data] data error')
        return 0
    already_working = 1
    if name == 'get: user_id':
        thread = Thread(target=get_info_by_user_id_and_, args=(user_id,))
        thread.start()
        thread.join()
    elif name == 'get: user_id, nickname':
        thread = Thread(target=get_info_by_user_id_and_, args=(user_id, nickname))
        thread.start()
        thread.join()
    elif name == 'get: user_id, nickname, password':
        thread = Thread(target=get_info_by_user_id_and_, args=(user_id, nickname, password))
        thread.start()
        thread.join()
    elif name == 'edit: auth_add':
        thread = Thread(target=edit_info_by_, args=('add_auth', user_id))
        thread.start()
        thread.join()
    elif name == 'edit: add_reg':
        thread = Thread(target=edit_info_by_, args=('add_reg', user_id, nickname, password))
        thread.start()
        thread.join()
    elif name == 'edit: del':
        thread = Thread(target=edit_info_by_, args=('del', user_id))
        thread.start()
        thread.join()
    elif name == 'find_friend':
        thread = Thread(target=find_in_friends, args=(user_id,))
        thread.start()
        thread.join()
    elif name == 'edit: minus_cash':
        thread = Thread(target=edit_info_by_, args=('minus_cash', user_id, None, None, cash))
        thread.start()
        thread.join()
    elif name == 'edit: plus_cash_txnId':
        thread = Thread(target=edit_info_by_, args=('plus_cash_txnId', user_id, None, None, cash, txnId))
        thread.start()
        thread.join()
    already_working = 0
    return result
