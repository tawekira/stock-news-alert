import requests
import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STOCK = "IBM"
COMPANY_NAME = "IBM"

stocks_api_key = os.environ["stocks_api_key"]
news_api_key = os.environ["news_api_key"]

my_email = os.environ["my_email"]
password = os.environ["password"]

stocks_parameters = {
    "function":"Time_Series_Daily",
    "symbol":STOCK,
    "apikey":stocks_api_key,
}

news_parameters = {
    "apiKey":news_api_key,
    "qInTitle":COMPANY_NAME,
    "language":"en"
}

response = requests.get("https://www.alphavantage.co/query", params = stocks_parameters)
response.raise_for_status()
print(response.text)
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_closing_price = float(data_list[0]["4. close"])
two_days_ago_closing_price = float(data_list[1]["4. close"])

difference = yesterday_closing_price - two_days_ago_closing_price
difference_formatted = str(round(difference, 2))
if difference>0:
    difference_formatted = "+"+difference_formatted

percentage = round(abs(difference)/two_days_ago_closing_price*100,2)

dates = []
for key in data:
    dates.append(key)
yesterday_date = dates[0]
two_days_ago_date = dates[1]
yesterday_closing_price = round(yesterday_closing_price, 2)
two_days_ago_closing_price = round(two_days_ago_closing_price, 2)


if percentage > 0:
    if difference>0:
        arrow = "🔺"
        color = "green"
    elif difference<0:
        arrow = "🔻"
        color = "red"

    reply = requests.get("https://newsapi.org/v2/everything", params= news_parameters)
    reply.raise_for_status()


    data = reply.json()["articles"]

    three_articles = []
    number = 0
    while len(three_articles)<3:
        if data[number]["urlToImage"] == None:
            number += 1

        else:
            three_articles.append(data[number])
            number += 1


    print(three_articles)
    title1 = three_articles[0]["title"]
    description1 = three_articles[0]["description"]
    url1 = three_articles[0]["url"]
    author1 = three_articles[0]["source"]["name"]
    picture1 = three_articles[0]["urlToImage"]
    date1 = three_articles[0]["publishedAt"].split("T")[0]

    title2 = three_articles[1]["title"]
    description2 = three_articles[1]["description"]
    url2 = three_articles[1]["url"]
    author2 = three_articles[1]["source"]["name"]
    picture2 = three_articles[1]["urlToImage"]
    date2 = three_articles[1]["publishedAt"].split("T")[0]

    title3 = three_articles[2]["title"]
    description3 = three_articles[2]["description"]
    url3 = three_articles[2]["url"]
    author3 = three_articles[2]["source"]["name"]
    picture3 = three_articles[2]["urlToImage"]
    date3 = three_articles[2]["publishedAt"].split("T")[0]

    html = f"""
            <html>
                <body>
                    <p style = "line-height: 1rem">{COMPANY_NAME} > {yesterday_date}</p>
                    <p><span style = "font-size: 2rem;font-weight: bold; line-height: 1rem">{yesterday_closing_price}</span><span style = "font-size: 1.2rem"> USD</span></p>
                    <p style = "color: {color}; line-height: 0.5rem">{difference_formatted} ({percentage}%)</p>
                    <hr>
            
                        <div>
                            <img src = {picture1} style = "width: 25%; height: 12rem; float: left; margin-right: 2%; margin-bottom: 2%; padding: 0px">
                            <div style = "float:  left; height: 12rem; width: 50%; margin-right: 23%; margin-bottom: 2%;">
                                <h6 style = "font-weight: normal; margin-bottom: 0; font-size: 0.8rem">{author1} · {date1}</h6>
                                <br>
                                <a href = {url1} style = "color: black; font-weight: bold">{title1}</a>
                                <p>{description1}</p>
                            </div>
                        </div>
                        <div>
                            <img src = {picture2} style = "width: 25%; height: 12rem; float: left; margin-right: 2%; margin-bottom: 2%; padding: 0px">
                            <div style = "float:  left; height: 12rem; width: 50%; margin-right: 23%; margin-bottom: 2%;">
                                <h6 style = "font-weight: normal; margin-bottom:0; font-size: 0.8rem">{author2} · {date2}</h6>
                                <br>
                                <a href = {url2} style = "color: black; font-weight: bold">{title2}</a>
                                <p>{description2}</p>
                            </div>
                        </div>
                        <div>
                            <img src = {picture3} style = "width: 25%; height: 12rem; float: left; margin-right: 2%; margin-bottom: 2%; padding: 0px">
                            <div style = "float:  left; height: 12rem; width: 50%; margin-right: 23%; margin-bottom: 2%;">
                                <h6 style = "font-weight: normal; margin-bottom:0; font-size: 0.8rem">{author3} · {date3}</h6>
                                <br>
                                <a href = {url3} style = "color: black; font-weight: bold">{title3}</a>
                                <p>{description3}</p>
                            </div>
                        </div>

                </body>
            </html>
            """

    email_message = MIMEMultipart()
    email_message["From"] = my_email
    email_message["To"] = "rayvialtan@gmail.com"
    email_message["Subject"] = f"{STOCK} {arrow}{percentage}%"
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()


    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user = my_email, password = password)
        connection.sendmail(from_addr = my_email, to_addrs = "rayvialtan@gmail.com", msg = email_string)


                                                                                           


