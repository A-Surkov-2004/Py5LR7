import time

class CurrenciesLst():

    def __init__(self):
        self.__cur_lst = [{
            'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')
        }, {
            'KZT': ('Казахстанских тенге', '19,8264')
        }, {
            'TRY': ('Турецких лир', '33,1224')
        }]


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
                valute[valute_charcode] = ('name":"'+str(valute_cur_name), 'value":"'+(value[0]), 'fractions":"'+(value[1]))
                result.append(valute)

        return result

    def get_currency(self, currency_id : str) -> list:

        if time.time() - self.last_time < self.delay:
            print(f'Please, wait {self.delay - (time.time() - self.last_time)} seconds')
            return [f'Please, wait {self.delay - (time.time() - self.last_time)} seconds']
        self.last_time = time.time()


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
            if str(valute_id) == currency_id:
                valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find(
                    'Value').text
                value = valute_cur_val.split(',')
                valute_charcode = _v.find('CharCode').text
                valute[valute_charcode] = ("name"+str(valute_cur_name), "value"+(value[0]), "fractions"+(value[1]))
                result.append(valute)

        if len(result):
            return result
        else:
            return [{'R9999': None}]


    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        val = []
        cur_lst = self.get_currencies()
        for el in cur_lst:
            key = str(el.keys())[12:15]
            currencies.append(key)
            val.append(el[key][1]+el[key][2]/pow(10, len(str(el[key][2]))))

        ax.bar(currencies, val)

        ax.set_ylabel('exchange rate')
        ax.set_title('visualized currencies')

        plt.show()





class MyClass(BaseClass, metaclass=Singleton):
    pass



if __name__ == '__main__':

    #res = get_currencies(['R01035', 'R01335', 'R01700J'])


    #CurrenciesLst.visualize_currencies(get_currencies(['R01035', 'R01335', 'R01700J']))

    mc = MyClass()
    mc.tracking_currencies = ['R01035', 'R01335', 'R01700J']
    print(mc.get_currencies())
    print(mc.get_currency('R01090B'))
    time.sleep(1)
    assert mc.get_currency('R01090A') == [{'R9999': None}]

    mc2 = MyClass()
    mc2.delay = 0

    assert mc.get_currency('R01090B')[0]['BYN'][0] == 'Белорусский рубль'

    mc2.tracking_currencies = ['R01625', 'R01720', 'R01820']
    assert mc.get_currencies()[2]['JPY'][0] == 'Японских иен'

    mc.visualize_currencies()