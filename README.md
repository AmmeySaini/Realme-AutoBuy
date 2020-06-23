# Realme-AutoBuy
This script will help you buy your favourite product from the sale by auto buying it for you

## ***Requirements***

- Python 3
- Python `pip`
- Python module `requests`
- Python module `browser_cookie3`
- Python module `bs4`
- Python module `argparse`

## ***Usage (Most Important)***
<b>Perform all these steps before sale</b>

Before sale you have to do some simple tasks in order to buy your product during sale.

First you need to login your account either in chrome or firefox browser(only specified browsers) or use cookie method (described below).

After logging in to your account, save the address in address.txt file in below format

`Your Name||Number without +91||pincode here||Street Address here||gmail id here||Landmark(if any)`

<b>`NOTE: Add valid number in address.txt as the same number will be verified with OTP during checking out`</b>

It will not work if the format is wrong. Then run `python cookie.py` and give name to your cookie file(unique)

<b>`NOTE: If you want to create cookies of multiple accounts you have to clear cookies of chrome or firefox for specific website (IF YOU LOGOUT COOKIES WILL EXPIRE)`</b>

- Tutorial to clear cookies from Chrome <a href='https://support.google.com/chrome/answer/95647'>Click Me</a>
- Tutorial to clear cookies from Firefox <a href='https://support.mozilla.org/en-US/kb/clear-cookies-and-site-data-firefox'>Click Me</a>

After you have created cookies make sure it's in my_cookies folder in project path.

Now run `python run.py`

It'll ask for all cookie files name and product id(or sale url). Enter all details and wait for sale to begin

Once sale begins hit enter it'll automatically add all your products to cart and you'll have 15 minutes to order it.

Wait for 1 minute and run `python order.py`

Now script will send OTP to your number(added in address.txt), verify it with correct OTP using script and your <b>ORDER WILL BE SUCCESSFUL</b>

***Run script***

    python run.py

## ***Module Installation***

	pip install -r requirements.txt

## ***Features***

- Generate cookies through the script itself
- Autobuy from multiple accounts
- Add address through script itself
- Single click and products will be added to your cart in all accounts
- Verify your OTP(s) using script only(saved your logging in part :) )

## ***Cookie Method***

<b>`Use this method only if script shows any error related using cookies method or if you don't have chrome or firefox browser`</b>

Firstly login to your account in website, now check cookies of the website

Copy `sessionId`, `opkey` and `newopkey` and save it in my_cookies folder with .txt example - `your_cookie_name.txt` in below format

`sessionId||opkey||newopkey` Now add address in address.txt as decribed above and run 

`python cookie.py -c your_cookie_name.txt`

After that follow the above steps to order it during sale
