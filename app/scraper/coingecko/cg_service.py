from pycoingecko import CoinGeckoAPI


class CgService(object):
    cg = CoinGeckoAPI()
    coin_list = cg.get_coins_list()

    def get_all_coins(self):
        return self.cg.get_coins_list()

    def get_coin_history(self, coin_name, history_date):
        try:
            coin_id = self.find_id(coin_name)
            return self.cg.get_coin_history_by_id(id=coin_id, date=history_date)
        except:
            return None

    def find_id(self, name):
        for coin in self.coin_list:
            if coin['name'] == name or coin['name'].lower() == name.lower() or coin['symbol'].lower() == name.lower():
                return coin['id']

    def get_price(self, ids):
        return self.cg.get_price(ids=ids, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true')