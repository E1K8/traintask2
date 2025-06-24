import pytest
import os
from processer import main


#Проверяем файл 
@pytest.fixture
def csv_file():
    filename = "products.csv"
    if not os.path.exists(filename):
        pytest.skip(f"Файл {filename} не найден")
    return filename


def test_filter_apple_products(csv_file, monkeypatch, capsys):
    #Фильтрация Apple
    inputs = [csv_file, "brand=apple", ""]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr()
    assert "iphone 15 pro" in captured.out
    assert "apple" in captured.out
    assert "samsung" not in captured.out


def test_avg_price(csv_file, monkeypatch, capsys):
    #Тест расчёта средней цены
    inputs = [csv_file, "", "avg=price"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr()
    assert "avg(price)" in captured.out
    assert "674.00" in captured.out  # (999+1199+199+299)/4 ≈ 674


def test_min_price_filtered(csv_file, monkeypatch, capsys):
    #поиск минимальной цены среди Xiaomi
    inputs = [csv_file, "brand=xiaomi", "min=price"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr()
    assert "min(price)" in captured.out
    assert "199" in captured.out  # Минимальная цена у Xiaomi
