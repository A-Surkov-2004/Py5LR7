from __future__ import annotations

import json
from src import curgetter
from abc import ABC, abstractmethod
from typing import List
from flask import Flask, render_template
from flask_socketio import SocketIO
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


class Subject(ABC):
    """
    Интерфейс издателя объявляет набор методов для управлениями подписчиками.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Отсоединяет наблюдателя от издателя.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class ConcreteSubject(Subject):
    """
    Издатель владеет некоторым важным состоянием и оповещает наблюдателей о его
    изменениях.
    """

    _state: int = None
    """
    Для удобства в этой переменной хранится состояние Издателя, необходимое всем
    подписчикам.
    """

    _observers: List[Observer] = []
    """
    Список подписчиков. В реальной жизни список подписчиков может храниться в
    более подробном виде (классифицируется по типу события и т.д.)
    """

    def __init__(self):
        self.data = None
        self.cc = curgetter.CurGetter()
        self.cc.delay = 0
        self.cc.tracking_currencies = ['R01235', 'R01239', 'R01375']

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    Методы управления подпиской.
    """

    def notify(self) -> None:
        """
        Запуск обновления в каждом подписчике.
        """

        print("Subject: Notifying observers...")
        socketio.emit('response', self.data)
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        """
        Обычно логика подписки – только часть того, что делает Издатель.
        Издатели часто содержат некоторую важную бизнес-логику, которая
        запускает метод уведомления всякий раз, когда должно произойти что-то
        важное (или после этого).
        """

        print("\nSubject: I'm doing something important.")

        cin = self.cc.get_currencies()
        now = json.loads(str(cin).replace('"', '').replace("'", '"').replace('(', '{').replace(')', '}'))

        self.data = f'USD:{now[0]['USD']['value']}.{now[0]['USD']['fractions']}, EUR:{now[1]['EUR']['value']}.{now[1]['EUR']['fractions']}, CNY:{now[2]['CNY']['value']}.{now[2]['CNY']['fractions']}'

        print(f"Subject: My state has just changed to: {self.data}")
        self.notify()


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


"""
Конкретные Наблюдатели реагируют на обновления, выпущенные Издателем, к которому
они прикреплены.
"""

app = Flask(__name__)

socketio = SocketIO(app)


@app.route('/USD')
def usd():
    return render_template('USD.html')


@app.route('/CNY')
def rub():
    return render_template('CNY.html')


@app.route('/EUR')
def eur():
    return render_template('EUR.html')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == "__main__":
    subject = ConcreteSubject()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=subject.some_business_logic, trigger="interval", seconds=5)
    scheduler.start()

    socketio.run(app, allow_unsafe_werkzeug=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
