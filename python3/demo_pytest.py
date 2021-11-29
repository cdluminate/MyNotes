import pytest

@pytest.mark.slow
def test_slow():
    pass

@pytest.mark.xxx
def test_xxx(tmpdir):
    print('tmpdir', tmpdir)
    pass

@pytest.mark.network
def test_network():
    pass

@pytest.mark.parametrize("arg1", ["xxx", "yyy", "zzz"])
def test_param(arg1):
    print(arg1)
    pass

@pytest.mark.parametrize("arg1, arg2",
        [(0, 1), (1,2), (3,4)]
        )
def test_param2(arg1, arg2):
    print(arg1, arg2)
    pass

@pytest.mark.exception
def test_except():
    with pytest.raises(ZeroDivisionError):
        x = 0/0

def test_assert():
    assert(True)

class TestClass(object):
    def test_1(self): pass
    def test_2(self): pass

'''
>>> pytest-3 demo_pytest.py -s -v
>>> pytest-3 demo_pytest.py -s -v -m network
>>> pytest-3 demo_pytest.py -s -v -k test_slow
>>> pytest-3 demo_pytest.py -s -v --durations=3
'''
