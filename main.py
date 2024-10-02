
import schedule
import time
from datetime import datetime, timedelta

from wsgiref import headers

from bs4 import BeautifulSoup
import requests
import lxml

import smtplib


def check_price():
    my_email = 'yashodhavemula09@gmail.com'
    my_password = 'xxxxxxxxxxxx'

    #url = input('Enter the url of the product whose price must be tracked.\n ')
    # assigning the url of the item to a variable
    url = "https://www.amazon.in/boAt-Airdopes-170-Playtime-Controls/dp/B0BSGQTVP1/ref=sr_1_6?crid=3JZMD5XAEF0J5&keywords=airpods&qid=1695832729&refinements=p_89%3AboAt&rnid=3837712031&s=electronics&sprefix=%2Caps%2C804&sr=1-6&th=1"
    # specifying the client's operating system and browser and the language to the server in order to make a request in
    # the mentioned language in an appropriate browser.
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
                      "Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    # to store the response into the  response variable and passing header request to it along with the url
    response = requests.get(url, headers=header)
    # (optional)either use another variable for saving the content as text,or invoke the function 'response.content' both
    # are same.
    # az_webpage=response.text
    # print(az_webpage)
    # Using beautiful soup to get hold of the content using lxml parser and making an object called 'soup'.
    soup = BeautifulSoup(response.content, "lxml")
    # Invoking the function "prettiffy()"to standardise the indentation of the printed script or code of the webpage.
    # print(soup.prettify())

    # BeautifulSoup is used to get hold of the price of the item from the webpage and is converted to floating point number.

    price = soup.find(name="span", class_="a-offscreen").getText()
    print(price)
    price_without_currency = price.split('₹')[1]
    price_before_comma = price_without_currency.split(',')[0]
    price_after_comma = price_without_currency.split(',')[1]
    price_in_string = price_before_comma+price_after_comma
    price_as_float = float(price_in_string)
    print(price_as_float)
    # to get the title of the product.
    title = soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break").getText()
    print(title)
    # setting the target price which the user can afford to.
    targetprice = 2000
    # message to be displayed if the price falls below the target price.
    # setting up the smtp module and the host and creating an object "connection" in order to invoke functions under smtplib

    if price_as_float < targetprice:
        message = f"{title}is now at {price}"
        # creates the smtp connection with gmail's smtp.
        with smtplib.SMTP('smtp.gmail.com') as connection:
            # the below line initiates a secure layer(Transport Layer Security) connection in order to send mail's
            # credentials securely.
            connection.starttls()
            # the below line is used to log in into my gmail account in order to compose gmail.
            connection.login(my_email, my_password)
            # sends the mail to the destination email address with relevant subject and message body.
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )







# Define your check_price function here
check_price()
