from calculator import calculator
import pytest


def test_type():
    calc = calculator.cal()
    with pytest.raises(Exception) as exc:
        calc.add(a=5, b='sf')
    assert "The information inputed is not a number. Closing Calculator!" in str(exc.value)


def test_add():
    calc = calculator.cal()
    assert calc.add(a=5, b=3) == 8


def test_sub():
    calc = calculator.cal()
    assert calc.sub(a=5, b=3) == 2


def test_multiply():
    calc = calculator.cal()
    assert calc.multiply(a=5, b=3) == 15


def test_divide():
    calc = calculator.cal()
    assert calc.divide(a=5, b=2) == 2.5
