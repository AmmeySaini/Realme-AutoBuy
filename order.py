import requests
import urllib3
import re
import time
from pathlib import Path
from __constants.constants import head1
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######### AUTHOR - @AmmeySaini #########
######### Github Repo -  https://github.com/AmmeySaini/Realme-AutoBuy #########
######### I'm not responisble for any damage or anything bad happens to you using this script #########
######### Use it on your own RISK #########
######### This is only for educational purpose #########

def main():
    total_orders = 0
    orders_file = Path('orders.txt')
    if orders_file.exists():
        with open(orders_file, 'r') as file:
            file_data = file.read()
        cookie_list = file_data.split('\n')
        for cooki in cookie_list:
            if cooki != '':
                cookie_file = Path('./my_cookies/' + cooki)
                if cookie_file.exists():
                    print('Performing on ' + cooki)
                    fp = open(cookie_file, 'r')
                    all_cooks = fp.read().split('||')
                    sessionId = all_cooks[0]
                    opkey = all_cooks[1]
                    newopkey = all_cooks[2]
                    cookie1 = dict(sessionId=sessionId, opkey=opkey, newopkey=newopkey)
                else:
                    print('cookie file doesn\'t exists')
            else:
                print('\nCompleted!!', 'Total Successful Orders - ' + str(total_orders))
                exit()

            url1 = 'https://api.realme.com/in/order/query'
            
            r = requests.get(url1, headers=head1, cookies=cookie1, verify=False)
            js = r.json()
            try:
                if len(js['data']) > 0:
                    try:
                        if js['data'][0]['orderStatus'] == 11 and js['data'][0]['countDown'] > 1:
                            orderNo = js['data'][0]['orderNo']
                            number = js['data'][0]['phone']
                            phoneAreacode = js['data'][0]['phoneAreacode']
                            url2 = 'https://api.realme.com/in/order/cod/verifyCode/sms'
                            data2 = '{"phoneNumber":"' + str(phoneAreacode) + str(number) + '","orderNo":"' + str(orderNo) + '"}'

                            r2 = requests.post(url2, headers=head1, data=data2, cookies=cookie1, verify=False)
                            js2 = r2.json()
                            if js2['msg'] == 'success':
                                verified = False
                                while verified != True:
                                    otp = int(input('Enter OTP sent to number ' + str(number + ': ')))
                                    url3 = 'https://api.realme.com/in/payment/custom/make-payment'
                                    data3 = '{"verifyCode":"' + str(otp) + '","orderNo":"' + str(orderNo) + '","payMethod":"COD","payChannel":"COD"}'
                                    r3 = requests.post(url3, headers=head1, data=data3, cookies=cookie1, verify=False)
                                    js3 = r3.json()
                                    if js3['code'] == 302:
                                        print('Order Successful', '\nSleeping for 1 Min, don\'t disturb me')
                                        total_orders += 1
                                        verified = True
                                        time.sleep(60)
                                    elif js3['code'] == 20133:
                                        print('Error - ' + js3['msg'])
                                        verified = False
                                    else:
                                        print('Error - ' + js3['msg'], '\nSleeping for 1 Min, don\'t disturb me')
                                        time.sleep(60)
                                        break
                            else:
                                print('Error - ' + js2['msg'], '\nSleeping for 1 Min, don\'t disturb me')
                                time.sleep(60)
                        elif js['data'][0]['orderStatus'] == 40:
                            print('Order is already processed')
                        else:
                            print('Error - Timeout Expired, Status is ' + str(js['data'][0]['orderStatus']))
                            # break
                    except Exception as e:
                        print(e)
            except:
                print('Error - Order does not exists')
    else:
        print('Error - Orders File doesn\'t exists')

if __name__ == '__main__':
    main()