import pytest

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

def test_suma():
    assert suma(2, 3) == 5
    assert suma(-1, 1) == 0
    assert suma(0, 0) == 0
    assert suma(3.5, 2.5) == 6.0

def test_resta():
    assert resta(7, 9) == 2
    assert resta(-2, 1) == 0
    assert resta(-1, 0) == -1
    assert resta(7.7, 2,7) == 5.0

def test_multiplicacion():
    assert multiplicacion(7, 9) == 2
    assert multiplicacion(-2, 1) == 0
    assert multiplicacion(-1, 0) == -1
    assert multiplicacion(7.7, 2,7) == 5.0

def test_division():
    assert division(7, 9) == 2
    assert division(-2, 1) == 0
    assert division(-1, 0) == -1
    assert division(7.7, 2,7) == 5.0

    with pytest.raises(ValueError, match="No se puede dividir por cero"):
        division(5, 0)

