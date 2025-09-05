import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

original_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
Amazon_URL = "https://appbrewery.github.io/instant_pot/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
  }

response = requests.get(original_url, headers=headers)
amazon_html = response.content

soup = BeautifulSoup(amazon_html, "html.parser")

price = soup.find(name="span", class_="aok-offscreen").getText()

price_without_currency = price.split("$")[1]
price_without_text = price_without_currency.split(" ")[0]

price_as_float = float(price_without_text)

title = soup.find(id="productTitle").getText().strip()

BUY_PRICE = 100
SMTP_ADDRESS = "smtp.gmail.com"

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price_as_float}!"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.ehlo()
        connection.starttls()
        result = connection.login(os.environ["EMAIL"], os.environ["PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL"],
            to_addrs=os.environ["EMAIL"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{Amazon_URL}".encode("utf-8")
        )



