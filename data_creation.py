import os


def init_file(id_user: int, column: int, row: int, confirm=False, field_density=500) -> bool:
    """
    Функция создания txt-файла в нужном виде
    :param id_user: id пользователя telegram
    :param column: количество столбцов
    :param row: количество строк
    :param confirm: подтверждение удаления файла, если он есть
    :param field_density: плотность поля
    :return: True - в случае успеха, False - в случае неудачи/ошибки
    """
    path = f'{id_user}.txt'
    # проверяем, есть ли файлик, ежели есть - разрешаем перезаписать
    if os.path.exists(path) and not confirm:
        os.remove(path)
        return False
    path = f'{id_user}.txt'

    with open(file=path, mode='w', encoding='utf-8') as file:
        lines = list()
        lines.append(f'{column}\t{row}\n')

        cur_line = ''
        for _ in range(column):
            cur_line += f'{field_density}\t'
        lines.append(cur_line + '\n')

        cur_line = ''
        for _ in range(row):
            cur_line += f'{field_density}\t'
        lines.append(cur_line + '\n')

        file.writelines(lines)
    return True


def fill_in(id_user: int, mas: list, x_size: int, y_size: int) -> bool:
    """
    Функция внесения данных введенные пользователем по строкам
    :param id_user: id пользователя в telegram
    :param columns: Список столбцов, в которые нужно поместить значение
    :param value: значение, вставленное на пересечении указанных строк и столбцов
    :param default_value: default'ное значение поля
    :return: True - в случае успеха, False - в случае неудачи/ошибки
    """
    path = f'{id_user}.txt'
    if not os.path.exists(path):
        return False
    with open(file=path, mode="a", encoding='utf-8') as file:
        line = ''
        for i in range(x_size):
            for j in range(y_size):
                line += f'{mas[i][j]}\t'
            file.write(line+'\n')
        return True
    return False

    # пользователю больше не надо вводить



if __name__ == "__main__":
    id = 12345
    columns = 5
    rows = 5


    if init_file(id_user=id, column=columns, row=rows, confirm=True):
        for row in range(rows):
            users_answer = list(input(f"Введите списком столбцы в {row+1} строке: ").replace(',', '').replace(' ', ''))
            value = int(input("Введите значение: "))
            fill_in(id_user=id, columns=users_answer, value=value)
