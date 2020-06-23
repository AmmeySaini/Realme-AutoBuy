import browser_cookie3
import requests
from pathlib import Path
import urllib3
import argparse
from __constants.constants import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######### AUTHOR - @AmmeySaini #########
######### Github Repo -  https://github.com/AmmeySaini/Realme-AutoBuy #########
######### I'm not responisble for any damage or anything bad happens to you using this script #########
######### Use it on your own RISK #########
######### This is only for educational purpose #########

def add_cookies(cck, name):
    global cookies
    sessionId=cck['sessionId']
    opkey=cck['opkey']
    newopkey=cck['newopkey']

    fp = open(Path('./my_cookies/' + name), 'w')
    fp.write(sessionId + '||' + opkey + '||' + newopkey)
    print('Cookie File Created')

def add_address(head, cck, namex):
    # global typeA
    addressFile = Path('address.txt')
    if addressFile.exists():
        fp = open(addressFile, 'r')
        add = fp.read().split('||')
        name = add[0]
        number = add[1]
        pincode = add[2]
        street = add[3]
        email = add[4]
        landmark = add[5]

        if name == 'Your Name':
            print('\nYou haven\'t added your address in address.txt file\nAdd your address to address.txt and then continue')
            exit()
        try:
            url2 = 'https://api.realme.com/in/user/address/check?pinCode=' + str(pincode)
            r = requests.get(url2, headers=head1, cookies=cck, verify=False)
            # print(r.text)
            js = r.json()
            cityName = js['data']['cityName']
            provinceName = js['data']['provinceName']
        except:
            print('\nWrong postalcode ' + str(pincode) + ' specified in address.txt')
            exit()

        url3 = 'https://api.realme.com/in/user/address/save'
        data3 = '{"provinceId":"","provinceName":"' + provinceName + '","cityName":"' + cityName + '","fullName":"' + name + '","postCode":"' + str(pincode) + '","phoneNumber":"' + str(number) + '","address1":"' + street + '","address2":"' + landmark + '","isDefault":1,"phoneCallingCodes":"+91","email":"' + email + '"}'
        r4 = requests.post(url3, headers=head1, data=data3, cookies=cck, verify=False)
        js2 = r4.json()
        if js2['msg'] == 'success':
            print('Address Successfully Added')
            if typeA == 0:
                add_cookies(cck, namex)
        else:
            print(js2['msg'])
    else:
        print('address file not found')
        exit()

def main():
    parser = argparse.ArgumentParser(description='', conflict_handler="resolve")
    authentication = parser.add_argument_group("Authentication")
    authentication.add_argument(
        '-c', '--cookies',\
        dest='cookies',\
        type=str,\
        help="Cookies to authenticate",metavar='')
    
    try:
        global typeA
        args = parser.parse_args()
        name = ''
        if args.cookies:
            cookie_file = Path('./my_cookies/' + args.cookies)
            if cookie_file.exists():
                typeA = 1
                print('Performing on ' + args.cookies)
                fp = open(cookie_file, 'r')
                all_cooks = fp.read().split('||')
                sessionId = all_cooks[0]
                opkey = all_cooks[1]
                newopkey = all_cooks[2]
                cck1 = ''
                cck = dict(sessionId=sessionId, opkey=opkey, newopkey=newopkey)
            else:
                print('Error - cookie file doesn\'t exists')
                exit()
        else:
            name = input('Enter name of cookie (make sure to give unique name everytime): ')
            if Path(name).is_file() == False:
                global cookies
                typeA = 0
                try:
                    cookies = browser_cookie3.load(domain_name='.realme.com')
                    cck1 = requests.utils.dict_from_cookiejar(cookies)
                except:
                    print('\nSorry to say but we are only working with chrome and firefox broswer\nInstall any of it to continue\nor use cookie method(check Readme on github)')
                    exit()
                sessionId=cck1['sessionId']
                opkey=cck1['opkey']
                newopkey=cck1['newopkey']
                cck = dict(sessionId=sessionId, opkey=opkey, newopkey=newopkey)
            else:
                print('Another file already exists with same name')

        url = 'https://api.realme.com/in/user/address/list'
        r2 = requests.get(url, headers=head1, cookies=cck, verify=False)
        js = r2.json()
        if len(js['data']['records']) > 0:
            for address in js['data']['records']:
                addID = address['id']

                url2 = 'https://api.realme.com/in/user/address/delete'
                data2 = '{"id":"' + addID + '","siteCode":"in"}'
                r3 = requests.post(url2, headers=head1, data=data2, cookies=cck, verify=False)
                js2 = r3.json()
                if js2['msg'] == 'success':
                    print('Removed old address ' + addID)
            add_address(head1, cck, name)
        else:
            add_address(head1, cck, name)
    except Exception as e:
        print(e, 'Please browse some more pages in website so that cookies can be captured/generated')


if __name__ == '__main__':
    main()