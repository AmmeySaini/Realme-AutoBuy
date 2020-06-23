import requests
import urllib3
from bs4 import BeautifulSoup
import browser_cookie3
import re
import argparse
from __constants.constants import *
from pathlib import Path
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######### AUTHOR - @AmmeySaini #########
######### Github Repo -  https://github.com/AmmeySaini/Realme-AutoBuy #########
######### I'm not responisble for any damage or anything bad happens to you using this script #########
######### Use it on your own RISK #########
######### This is only for educational purpose #########

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def main():
    parser = argparse.ArgumentParser(description='', conflict_handler="resolve")
    authentication = parser.add_argument_group("Authentication")
    authentication.add_argument(
        '-c', '--cookies',\
        dest='cookies',\
        type=str,\
        help="Cookies to authenticate",metavar='')
    authentication.add_argument(
        '-id', '--id',\
        dest='id',\
        type=str,\
        help="ID of product",metavar='')

    try:
        args = parser.parse_args()
        if args.cookies and args.id:
            id__ = args.id
            pCFile = args.cookies
            cookie_file = Path('./my_cookies/' + pCFile)
            print('Performing on ' + pCFile)
            if cookie_file.exists():
                fp = open(cookie_file, 'r')
                all_cooks = fp.read().split('||')
                sessionId = all_cooks[0]
                opkey = all_cooks[1]
                newopkey = all_cooks[2]
                cooki = dict(sessionId=sessionId, opkey=opkey, newopkey=newopkey)
            else:
                print('cookie file doesn\'t exists')
                exit()
        else:
            print('cookies and id param is needed')
            exit()
    except Exception as e:
        print(e, 'some error fetching cookie file')
        exit()


    url3 = 'https://api.realme.com/in/product/detail?productId=' + id__
    r2 = requests.get(url3, headers=head1, cookies=cooki, verify=False)
    js1 = r2.json()
    if js1['msg'] == 'success':

        cc = js1['data'].keys()
        first = list(cc)[0]
        skuId = js1['data'][first]['skuId']
        price = js1['data'][first]['price']
        productName = js1['data'][first]['productName']
        skuName = js1['data'][first]['skuName']
        skuName = skuName.replace(productName, '')
        dd = skuName[1:]
        ll = {'(': '', ')': '', ',': ' '}
        final_sku = replace_all(dd, ll)
        # for keys in js1['data'].keys():
        #     print(keys)
        final_sku = re.sub(r'[^\x00-\x7f]',r' ', final_sku) 
        productName = re.sub(r'[^\x00-\x7f]',r' ', productName) 
        url2 = 'https://api.realme.com/in/order/purchase/checkout'

        datax = '{"ignoreAdditionNos": [],"skuList": [{"skuId": ' + str(skuId) + ',"price": ' + str(price) +',"skuName": "' + str(final_sku) + '","productName": "' + productName + '","count": 1,"giftNos": [],"packageNos": [],"limitOfferCode": ""}],"realmeCode": "","purchaseType": 1,"pincode": ""}'

        r3 = requests.post(url2, headers=head1, cookies=cooki, data=datax, verify=False)

        js2 = r3.json()

        try:
            if js2['msg'] == 'success':
                print('Successfully Added To Cart')

                url5 = 'https://api.realme.com/in/user/address/list'

                r5 = requests.get(url5, headers=head1, cookies=cooki, verify=False)
                js3 = r5.json()    
                try:
                    addressID = js3['data']['records'][0]['id']
                    print('Successfully fetched address id')
                except:
                    print('error while fetching Address id')
                    addressID = ''
                
                if addressID != '':
                    url6 = 'https://api.realme.com/in/order/purchase/create'
                    data6 = '{"addressId":"' + addressID + '","prizeType":"","prizeCode":"","invoiceCategory":1,"invoiceTitle":"","invoiceTaxNo":"","purchaseType":"1","ignoreAdditionNos":[],"quoteUid":"","payMode":""}'
                    r4 = requests.post(url6, data=data6, headers=head1, cookies=cooki, verify=False)
                    js4 = r4.json()
                    try:
                        if js4['msg'] == 'success':
                            print('you have 15 mins to order\nOrder id is: ' + str(js4['data']))
                            fp = open('orders.txt', 'w')
                            fp.write(pCFile + '\n')
                    except:
                        print('error while checking out')
                else:
                    print('address id is empty')
            else:
                print(js2['msg'])
        except:
            print('error ' + js2['msg'])
    else:
        print(js1['msg'])
if __name__ == '__main__':
    main()