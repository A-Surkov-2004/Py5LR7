import time


class CurrenciesLst():

    def __init__(self):
        pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseClass:
    def __init__(self):
        self._tracking_currencies = []
        self.last_time = 0
        self.delay = 1

    def get_tracking_currencies(self):
        return self._tracking_currencies
        # using the set function

    def set_tracking_currencies(self, y):
        self._tracking_currencies = y
        # using the del function

    def del_tracking_currencies(self):
        del self._tracking_currencies

    tracking_currencies = property(get_tracking_currencies, set_tracking_currencies, del_tracking_currencies)

    def set_delay(self, seconds):
        self.delay = seconds

    def get_currencies(self) -> list:

        if time.time() - self.last_time < self.delay:
            print(f'Please, wait {self.delay - (time.time() - self.last_time)} seconds')
            return [f'Please, wait {self.delay - (time.time() - self.last_time)} seconds']
        self.last_time = time.time()

        currencies_ids_lst = self.tracking_currencies

        import requests
        from xml.etree import \
            ElementTree as ET

        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        result = []

        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall(
            "Valute"
        )
        for _v in valutes:
            valute_id = _v.get('ID')
            valute = {}
            if (str(valute_id) in currencies_ids_lst):
                valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find(
                    'Value').text
                value = valute_cur_val.split(',')
                valute_charcode = _v.find('CharCode').text
                valute[
                    valute_charcode] = f'''('name':'{valute_cur_name}', 'value':'{value[0]}', 'fractions':'{value[1]}')'''
                result.append(valute)

        if len(result):
            return result
        else:
            return [{'R9999': None}]


class CurGetter(BaseClass, metaclass=Singleton):
    pass
