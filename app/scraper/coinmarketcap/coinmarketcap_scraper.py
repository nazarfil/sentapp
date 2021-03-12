#!/usr/bin/python3
# coding: utf-8
from app import log

import requests
from bs4 import BeautifulSoup
from scrapy import Selector
import csv
import datetime
import cfscrape

logger = log.setup_custom_logger('scraper')
def extract(url):
    session = requests.session()
    start = datetime.datetime.now()
    for retry in range(10):
        scraper = cfscrape.create_scraper(sess=session, delay=10)
        response = scraper.get(url=url)

        if response.status_code == 200:
            with open("cryptocurrencies_{}.csv".format(str(datetime.date.today())), "w+") as f:
                logger.info("Printing to file")
                fieldnames = ['id', 'name', 'ticker', 'price', 'market_cap']
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()

                soup = BeautifulSoup(response.content, features='html.parser')
                sel = Selector(text=soup.prettify())
                cryptos = sel.xpath("//tr").extract()
                cryptos2 = cryptos[3:53]
                for crypto in cryptos2:
                    soup = BeautifulSoup(crypto, features='html.parser')
                    sel = Selector(text=soup.prettify())

                    id = sel.xpath("//td[1]/div/text()").extract_first()
                    nom = sel.xpath("//td[2]/div/a/text()").extract_first()
                    symbole = sel.xpath("//td[3]/div/text()").extract_first()
                    price = sel.xpath("//td[4]/p/text()").extract_first()
                    market_cap = sel.xpath("//td[5]/div/a/text()").extract_first()
                    clean_values = []
                    values = [id, nom, symbole, price, market_cap]
                    for value in values:
                        if value:
                            value = value.strip().replace('\n', '')
                        clean_values.append(value)

                    dict_row = dict(zip(fieldnames, clean_values))
                    writer.writerow(dict_row)

            end = datetime.datetime.now()
            time_elapsed = str(end - start)
            logger.info('\n')
            logger.info('-- TIME ELAPSED --')
            logger.info(time_elapsed)
            break


def extract_to_mem():
    url = "https://coinmarketcap.com/all"
    session = requests.session()
    result_cryptos = []
    for retry in range(10):
        scraper = cfscrape.create_scraper(sess=session, delay=10)
        response = scraper.get(url=url)
        if response.status_code == 200:
            fieldnames = ['id', 'name', 'ticker', 'price', 'market_cap']

            soup = BeautifulSoup(response.content, features='html.parser')
            sel = Selector(text=soup.prettify())
            cryptos = sel.xpath("//tr").extract()
            cryptos2 = cryptos[3:53]
            for crypto in cryptos2:
                soup = BeautifulSoup(crypto, features='html.parser')
                sel = Selector(text=soup.prettify())

                id = sel.xpath("//td[1]/div/text()").extract_first()
                nom = sel.xpath("//td[2]/div/a/text()").extract_first()
                symbole = sel.xpath("//td[3]/div/text()").extract_first()
                market_cap = sel.xpath("//td[4]/p/text()").extract_first()
                price = sel.xpath("//td[5]/div/a/text()").extract_first()
                values = dict({'id': id.strip().replace('\n', ''),
                               'name': nom.strip().replace('\n', ''),
                               'ticker': symbole.strip().replace('\n', ''),
                               'price': price.strip().replace('\n', ''),
                               'market_cap': market_cap.strip().replace('\n', '')})
                result_cryptos.append(values)
            break
    return result_cryptos


def main():
    url = "https://coinmarketcap.com/all"
    extract(url)


if __name__ == '__main__':
    main()
