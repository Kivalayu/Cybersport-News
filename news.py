import textwrap
import aiohttp
import asyncio
import telebot
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

API_KEY = '5713032589:AAEojXFEZWVvkVjSN4J_C9LBINq2_W7Zz9U'
BASE_URL = "https://www.cybersport.ru/tags/dota-2"
BASE_URL1 = "https://www.cybersport.ru/tags/cs-go"
HEADERS = {"User-Agent": UserAgent().random}


async def fetch_news():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            html = await response.text()
            soup = bs(html, "html.parser")
            links = soup.find_all('div', {"class": "rounded-block root_d51Rr with-hover no-padding no-margin"})
            news = []
            for link_container in links:
                link_element = link_container.find('a', {"class": "link_CocWY"})
                if link_element is None:
                    continue
                link = link_element.get("href")
                news_element = link_container.find('h3', {"class": "title_nSS03"})
                if news_element is None:
                    continue
                headline = news_element.text.strip()
                news.append(f"{headline} | https://www.cybersport.ru{link}")
            return news

async def fetch_news1():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL1, headers=HEADERS) as response:
            html = await response.text()
            soup = bs(html, "html.parser")
            links = soup.find_all('div', {"class": "rounded-block root_d51Rr with-hover no-padding no-margin"})
            news1 = []
            for link_container in links:
                link_element = link_container.find('a', {"class": "link_CocWY"})
                if link_element is None:
                    continue
                link = link_element.get("href")
                news1_element = link_container.find('h3', {"class": "title_nSS03"})
                if news1_element is None:
                    continue
                headline = news1_element.text.strip()
                news1.append(f"{headline} | https://www.cybersport.ru{link}")
            return news1

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Hello! To get CS:GO or DOTA 2 news, type /csgonews or /dotanews:')

@bot.message_handler(commands=['dotanews'])
def newss(message):
    if message.text.lower().startswith('/news'):
        news = asyncio.run(fetch_news())
        news_str = 'You requested DOTA 2 news. Here are the latest updates:\n\n' + '\n\n'.join(news)
        news_list = textwrap.wrap(news_str, width=4000, replace_whitespace=False)
        for i, news_part in enumerate(news_list, start=1):
            bot.send_message(message.chat.id, f"{i}/{len(news_list)}: {news_part}")
    else:
        bot.send_message(message.chat.id, 'Something went wrong! Please type /news to get the latest DOTA 2 news.')


@bot.message_handler(commands=['csgonews'])
def newss(message):
    if message.text.lower().startswith('/csgonews'):
        news1 = asyncio.run(fetch_news1())
        news_str = 'You requested CS:GO news. Here are the latest updates:\n\n' + '\n\n'.join(news1)
        news_list = textwrap.wrap(news_str, width=4000, replace_whitespace=False)
        for i, news_part in enumerate(news_list, start=1):
            bot.send_message(message.chat.id, f"{i}/{len(news_list)}: {news_part}")
    else:
        bot.send_message(message.chat.id, 'Something went wrong! Please type /news to get the latest CS:GO news.')

bot.polling()
