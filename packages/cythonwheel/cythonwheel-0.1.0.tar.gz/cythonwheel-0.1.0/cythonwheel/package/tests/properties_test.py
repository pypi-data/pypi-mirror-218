from cythonwheel.package import Holder

def test_some_properties():
    a = 5
    assert a == 5


def test_holder():
    h = Holder(5)

    assert h.a == 5
