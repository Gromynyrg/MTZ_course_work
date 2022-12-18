import os


def init_file(id_user: int, column: int, row: int, field_density=500) -> bool:
    """
    Функция создания txt-файла в нужном виде
    :param id_user: id пользователя telegram
    :param column: количество столбцов
    :param row: количество строк
    :param field_density: плотность поля
    """
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
    :param mas: массив данных для вывода файла
    :param x_size & y_size размеры массива
    """
    path = f'{id_user}.txt'
    if not os.path.exists(path):
        return False
    with open(file=path, mode="a", encoding='utf-8') as file:

        for i in range(x_size):
            line = ''
            for j in range(y_size):
                line += f'{mas[i][j]}\t'
            file.write(line+'\n')
        return True
    return False

    # пользователю больше не надо вводить



