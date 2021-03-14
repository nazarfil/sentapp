from pycoingecko import CoinGeckoAPI


class CgService(object):
    cg = CoinGeckoAPI()

    def get_all_coins(self):
        return self.cg.get_coins_list()

    def get_coin_history(self, coin_id, history_date):
        try:
            return self.cg.get_coin_history_by_id(id=coin_id, date=history_date)
        except:
            return None
