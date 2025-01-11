from src import curgetter
import time


def test1():
    # given
    mc = curgetter.CurGetter()
    mc.delay = 0
    mc.tracking_currencies = ['R01035', 'R01335', 'R01700J']

    # when
    ans = mc.get_currencies()

    # then
    assert (list(ans[0].keys())) == ['GBP']
    assert (list(ans[1].keys())) == ['KZT']
    assert (list(ans[2].keys())) == ['TRY']


def test2():
    # given
    mc = curgetter.CurGetter()
    mc.delay = 0
    cur = 'Hello world'
    mc.tracking_currencies = ['Hello world']

    # when
    ans = mc.get_currencies()

    # then
    assert ans == [{'R9999': None}]


def test3():
    # given
    mc1 = curgetter.CurGetter()
    mc2 = curgetter.CurGetter()
    mc2.delay = 0
    mc1.delay = 1
    time.sleep(1)
    mc1.tracking_currencies = ['R01035']

    # when
    ans1 = mc1.get_currencies()
    ans2 = mc2.get_currencies()

    # then
    print(ans2)
    assert (list(ans1[0].keys())) == ['GBP']
    assert type(ans2[0]) == str  # 'Please, wait n seconds'
    mc1.delay = 0


test1()
test2()
test3()
