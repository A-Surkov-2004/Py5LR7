

import curgetter
import json
import io
import csv
from abc import ABC, abstractmethod


class Component(ABC):

    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется
    декораторами.
    """

    @abstractmethod
    def get_currencies(self):
        pass

    @abstractmethod
    def get_currency(self, cid):
        pass


class ConcreteComponent(Component):

    def __init__(self):
        self.cc = curgetter.MyClass()
        self.cc.delay = 0
        self.cc.tracking_currencies = ['R01235', 'R01239', 'R01375']

    def get_currencies(self):
        return self.cc.get_currencies()

    def get_currency(self, cid):
        return self.cc.get_currency(cid)
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может
    быть несколько вариаций этих классов.
    Для нашей программы ConcreteComponent - Класс возвращающий dict
    """


    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> str:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._component

    def operation(self) -> str:
        return self._component.operation()

    def get_currencies(self):
        self._component.get_currencies()
        return self._component.get_currencies()

    def get_currency(self, cid):
        return  self._component.get_currency(cid)




class ConcreteDecoratorA(Decorator):
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    Для нашей программы ConcreteDecoratorA - Класс возвращающий json
    """


    def operation(self) -> str:


        """
        Декораторы могут вызывать родительскую реализацию операции, вместо того,
        чтобы вызвать обёрнутый объект напрямую. Такой подход упрощает
        расширение классов декораторов.
        """
        return f"ConcreteDecoratorA({self.component.operation()})"

    def get_currencies(self):

        cin = self.component.get_currencies()
        if str(type(cin)) == "<class 'str'>":

            v = cin.split('\r\n')
            for i in range(len(v)):
                v[i] = v[i].split(',')
            ans = []

            for i in v:
                if len(i) == 4:
                    string1 = f'["{i[0]}": ["name": "{i[1]}", "value": "{i[2]}", "fractions": "{i[3]}"]]'
                    ans.append(string1.replace('[', '{').replace(']', '}'))
            return json.loads(str(ans).replace("'", ''))
        else:

            ans = json.loads(str(cin).replace("'", '"').replace('(', '{').replace(')', '}'))
            return ans






class ConcreteDecoratorB(Decorator):

    """
    Декораторы могут выполнять своё поведение до или после вызова обёрнутого
    объекта.
    Для нашей программы ConcreteDecoratorB - Класс возвращающий csv
    """
    def get_currencies(self):
        data = json.loads(str(self.component.get_currencies()).replace("'",'"').replace('(','{').replace(')','}'))

        csv_buffer = io.StringIO()

        new_row = ['code', 'name', 'value', 'fractions']
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(new_row)

        for cur in data:

            code = list(cur.keys())[0]
            name = cur[code]['name']
            value = cur[code]['value']
            fractions = cur[code]['fractions']
            new_row = [code,name,value,fractions]
            csv_writer.writerow(new_row)

        return csv_buffer.getvalue()



    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component: Component) -> None:
    """
    Клиентский код работает со всеми объектами, используя интерфейс Компонента.
    Таким образом, он остаётся независимым от конкретных классов компонентов, с
    которыми работает.
    """

    # ...

    ans = component.get_currencies()

    ans = json.loads(str(ans).replace('(','{').replace(')', '}').replace("'",'"'))

    return ans
    # ...

def getjson():
    simple = ConcreteComponent()
    return client_code(simple)


if __name__ == '__main__':

    # Таким образом, клиентский код может поддерживать как простые компоненты...
    simple = ConcreteComponent()
    print("Client: I've got a simple component:")
    asn =     client_code(simple)

    print("\n")

    # # ...так и декорированные.
    # #
    # # Обратите внимание, что декораторы могут обёртывать не только простые
    # # компоненты, но и другие декораторы.
    decorator1 = ConcreteDecoratorA(simple)
    decorator2 = ConcreteDecoratorB(decorator1)

    print("Client: Now I've got a decorated component:")
    client_code(decorator2)

    print('Back to json')
    dec3 = ConcreteDecoratorA(decorator2)
    client_code(dec3)
