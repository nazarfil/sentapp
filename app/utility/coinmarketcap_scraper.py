#!/usr/bin/python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from scrapy import Selector
import csv
import datetime
import cfscrape


def extract(url):
    session = requests.session()
    start = datetime.datetime.now()
    for retry in range(10):
        scraper = cfscrape.create_scraper(sess=session, delay=10)
        response = scraper.get(url=url)

        if response.status_code == 200:
            with open("cryptocurrencies_{}.csv".format(str(datetime.date.today())), "w+") as f:
                print("Printing to file")
                fieldnames = ['id', 'name', 'ticker']
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()

                soup = BeautifulSoup(response.content, features='html.parser')
                sel = Selector(text=soup.prettify())
                cryptos = sel.xpath("//tr").extract()
                cryptos2 = cryptos[3:50]
                for crypto in cryptos2:
                    soup = BeautifulSoup(crypto, features='html.parser')
                    sel = Selector(text=soup.prettify())

                    id = sel.xpath("//td[1]/div/text()").extract_first()
                    nom = sel.xpath("//td[2]/div/a/text()").extract_first()
                    symbole = sel.xpath("//td[3]/div/text()").extract_first()
                    clean_values = []
                    values = [id, nom, symbole]
                    for value in values:
                        if value:
                            value = value.strip().replace('\n', '')
                        clean_values.append(value)

                    dict_row = dict(zip(fieldnames, clean_values))
                    print(dict_row)
                    writer.writerow(dict_row)

            end = datetime.datetime.now()
            time_elapsed = str(end - start)
            print('\n')
            print('-- TIME ELAPSED --')
            print(time_elapsed)
            break


def main():
    url = "https://coinmarketcap.com/all"
    extract(url)


if __name__ == '__main__':
    main()
