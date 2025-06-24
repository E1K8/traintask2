import csv
from tabulate import tabulate


def main():
    path = input("Введите путь к файлу: ")
    fill = input("Введите условие для фильтрации: ")
    agrr = input("Введите условие для агрегации: ")

    # Чтение
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    headers = data[0]
    rows = data[1:]

    # Фильтрация
    if fill:
        if '>=' in fill:
            col, val = fill.split('>=')
            op = '>='
        elif '<=' in fill:
            col, val = fill.split('<=')
            op = '<='
        elif '>' in fill:
            col, val = fill.split('>')
            op = '>'
        elif '<' in fill:
            col, val = fill.split('<')
            op = '<'
        elif '=' in fill:
            col, val = fill.split('=')
            op = '='
        else:
            print("Неверный формат условия фильтрации")
            return

        col = col.strip()
        val = val.strip()

        #  фильтрацию
        filtered_rows = []
        for row in rows:
            row_dict = dict(zip(headers, row))
            try:
                # Пробуем сравнить как числа
                cell_val = float(row_dict[col])
                filter_val = float(val)
            except ValueError:
                # сравниваем как строки
                cell_val = row_dict[col]
                filter_val = val

            if op == '=' and cell_val == filter_val:
                filtered_rows.append(row)
            elif op == '>' and cell_val > filter_val:
                filtered_rows.append(row)
            elif op == '<' and cell_val < filter_val:
                filtered_rows.append(row)
            elif op == '>=' and cell_val >= filter_val:
                filtered_rows.append(row)
            elif op == '<=' and cell_val <= filter_val:
                filtered_rows.append(row)

        rows = filtered_rows

    # Агрегация
    if agrr:
        if '=' not in agrr:
            print("Неверный формат условия агрегации")
            return

        func, col = agrr.split('=')
        func = func.strip().lower()
        col = col.strip()

        if func not in ['avg', 'min', 'max']:
            print("Доступные функции агрегации: avg, min, max")
            return

        try:
            col_index = headers.index(col)
        except ValueError:
            print(f"Колонка '{col}' не найдена")
            return

        values = []
        for row in rows:
            try:
                values.append(float(row[col_index]))
            except ValueError:
                print(f"Ошибка: колонка '{col}' содержит не числовые значения")
                return

        if func == 'avg':
            result = sum(values) / len(values)
        elif func == 'min':
            result = min(values)
        elif func == 'max':
            result = max(values)

        print("\nРезультат агрегации:")
        print(f"{func}({col}) = {result:.2f}" if func == 'avg' else f"{func}({col}) = {result}")
    else:
        print("\nРезультат фильтрации:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()