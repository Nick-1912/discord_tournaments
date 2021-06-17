import requests
import json
import data_methods
import time


class QIWI(object):
    def __init__(self, token, login):
        self.token = token
        self.login = login

    def payment_history_last(self, rows_num, next_TxnId, next_TxnDate):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.token
        parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate}
        h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + self.login + '/payments', params=parameters)
        return h.json()

    def get_history(self):
        qiwi_history = self.payment_history_last('20', '', '')
        history = []
        for his in qiwi_history['data']:
            history.append(
                {'nickname': str(his['comment']), 'cash': str(his['sum']['amount']), 'txnId': str(his['txnId'])})
        return history

    def send_p2p(self, to_qw, sum_p2p):
        s = requests.Session()
        s.headers = {'content-type': 'application/json'}
        s.headers['authorization'] = 'Bearer ' + self.token
        s.headers['User-Agent'] = 'Android v3.2.0 MKT'
        s.headers['Accept'] = 'application/json'
        postjson = {"id": "", "sum": {"amount": "", "currency": ""},
                    "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "'+comment+'",
                    "fields": {"account": ""}}
        postjson['id'] = str(int(time.time() * 1000))
        postjson['sum']['amount'] = sum_p2p
        postjson['sum']['currency'] = '643'
        postjson['fields']['account'] = to_qw
        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
        return res.json()


def update_cash(user_id):
    q = QIWI(token='-', login='-')
    history = q.get_history()
    result = data_methods.start_method(name='get: user_id',
                                       user_id=user_id)
    for history_element in history:
        if history_element['nickname'] == result['nickname'] and history_element['txnId'] != result['txnId']:
            data_methods.start_method(name='edit: plus_cash_txnId',
                                      user_id=user_id, cash=history_element['cash'],
                                      txnId=history_element['txnId'])
            break
    else:
        print('[cash] user no payment')


def send_cash(user_id, cash):
    q = QIWI(token='-', login='-')
    result = data_methods.start_method(name='get: user_id',
                                       user_id=user_id)
    q.send_p2p(to_qw=result['number'], sum_p2p=cash)
