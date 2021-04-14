import pygame
import sys
from random import *
import time

def generateField():  # Генерация поля
    field = []
    for i in range(4):
        field.append([])
        for j in range(4):
            field[i].append(0)
    return field

def generateListEmpty(field):  # Генерация списка пустых ячеек
    empty = []
    for i in range(4):
        for j in range(4):
            if (field[i][j] == 0):
                empty.append([i, j])
    return empty

def insertNumber(field, empty):  # Вставить 2 или 4 рандомно
    ix = randint(0, len(empty) - 1)
    if (randint(1, 5) == 1):
        field[empty[ix][0]][empty[ix][1]] = 4
    else:
        field[empty[ix][0]][empty[ix][1]] = 2

def drawInterface():  # Графический интерфейс
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont("stxingkai", 70)
    #text = font.render(f'{"score: ")}', True, BLACK)
    #text_x = 25
    #text_y = 110 / 3
    #screen.blit(text, (text_x, text_y))
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = field[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if (value != 0):
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))

def moveLeft(field):  # Обработчик левого нажатия
    for row in field:
        while (0 in row):
            row.remove(0)
        while (len(row) != 4):
            row.append(0)
    for i in range(4):
        for j in range(4 - 1):
            if ((field[i][j] == field[i][j + 1]) and (field[i][j] != 0)):
                field[i][j] *= 2
                field[i].pop(j + 1)
                field[i].append(0)
    return field

def moveRight(field): # Обработчик правого нажатия
    for row in field:
        while (0 in row):
            row.remove(0)
        while (len(row) != 4):
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if ((field[i][j] == field[i][j - 1]) and (field[i][j] != 0)):
                field[i][j] *= 2
                field[i].pop(j - 1)
                field[i].insert(0, 0)
    return field

def moveUp(field): # Обработчик верхнего нажатия
    for column in range(4):
        temp_list = []
        for row in range(4):
            temp_list.append(field[row][column])
        while (0 in temp_list):
            temp_list.remove(0)
        while (len(temp_list) != 4):
            temp_list.append(0)
        for i in range(3):
            if ((temp_list[i] == temp_list[i + 1]) and (temp_list[i] != 0)):
                temp_list[i] *= 2
                temp_list.pop(i + 1)
                temp_list.append(0)
        for row in range(4):
            field[row][column] = temp_list[row]
    return field

def moveDown(field): # Обработчик нижнего нажатия
    for column in range(4):
        temp_list = []
        for row in range(4):
            temp_list.append(field[row][column])
        while (0 in temp_list):
            temp_list.remove(0)
        while (len(temp_list) != 4):
            temp_list.insert(0, 0)
        for i in range(3, 0, -1):
            if ((temp_list[i] == temp_list[i - 1]) and (temp_list[i] != 0)):
                temp_list[i] *= 2
                temp_list.pop(i - 1)
                temp_list.insert(0, 0)
        for row in range(4):
            field[row][column] = temp_list[row]
    return field

def canMove(field): # Можно ли передвигаться
    res = [False, False, False, False]
    for row in range(4): # Движение влево
        for column in range(4):
            if (field[row][column] != 0):
                if (column < 3):
                    if (field[row][column] == field[row][column+1]):
                        res[0] = True
                        break
                    else:
                        continue
            else:
                if (column < 3):
                    if (field[row][column+1] == 0):
                        continue
                    else:
                        res[0] = True
                        break
        if (res[0]):
            break

    for row in range(4): # Движение вправо
        for column in range(3, -1, -1):
            if (field[row][column] != 0):
                if (column > 0):
                    if (field[row][column] == field[row][column-1]):
                        res[1] = True
                        break
                    else:
                        continue
            else:
                if (column > 0):
                    if (field[row][column-1] == 0):
                        continue
                    else:
                        res[1] = True
                        break
        if (res[1]):
            break

    for column in range(4): # Движение вверх
        for row in range(4):
            if (field[row][column] != 0):
                if (row < 3):
                    if (field[row][column] == field[row+1][column]):
                        res[2] = True
                        break
                    else:
                        continue
            else:
                if (row < 3):
                    if (field[row+1][column] == 0):
                        continue
                    else:
                        res[2] = True
                        break
        if (res[2]):
            break

    for column in range(4): # Движение вниз
        for row in range(3, -1, -1):
            if (field[row][column] != 0):
                if (row > 0):
                    if (field[row][column] == field[row-1][column]):
                        res[3] = True
                        break
                    else:
                        continue
            else:
                if (row > 0):
                    if (field[row-1][column] == 0):
                        continue
                    else:
                        res[3] = True
                        break
        if (res[3]):
            break

    return res

def highest(field): # Возвращает наибольшее число на поле
    res = 0
    for i in range(4):
        for j in range(4):
            if (field[i][j] > res):
                res = field[i][j]
    return res

def emptyCount(field):
    count = 0
    for i in field:
        for j in i:
            if (j == 0):
                count += 1
    return count

def monotonicity(field):
    res = 8
    temp = 100000
    for row in range(4):
        for col in range(3):
            if (field[row][col] != 0):
                temp = field[row][col]
            if (temp <= field[row][col+1]):
                res -= 1
                break
        temp = 100000
    for col in range(4):
        for row in range(3):
            if (field[row][col] != 0):
                temp = field[row][col]
            if (temp <= field[row+1][col]):
                res -= 1
                break
        temp = 100000
    return res

def smoothness(field):
    res = 0
    for row in range(4):
        for col in range(3):
            if ((field[row][col] == field[row][col+1]) and (field[row][col] != 0)):
                res += 1
    for col in range(4):
        for row in range(3):
            if ((field[row][col] == field[row+1][col]) and (field[row][col] != 0)):
                res += 1

    return res

def sum(field): # Сумма всех ячеек
    res = 0
    for i in range(4):
        for j in range(4):
            res += field[i][j]
    return res

def count_numbers(field): # Количество ячеек каждого номинала на поле
    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            if (field[i][j] == 2048):
                res[0] += 1
            if (field[i][j] == 1024):
                res[1] += 1
            if (field[i][j] == 512):
                res[2] += 1
            if (field[i][j] == 256):
                res[3] += 1
            if (field[i][j] == 128):
                res[4] += 1
            if (field[i][j] == 64):
                res[5] += 1
            if (field[i][j] == 32):
                res[6] += 1
            if (field[i][j] == 16):
                res[7] += 1
            if (field[i][j] == 8):
                res[8] += 1
            if (field[i][j] == 4):
                res[9] += 1
            if (field[i][j] == 2):
                res[10] += 1
    return res

def count_exp(list): # Количество ячеек каждого номинала в результате множества симуляций (берется максимальная фишка из симуляуции)
    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(list)):
        if (list[i] == 2048):
            res[0] += 1
        if (list[i] == 1024):
            res[1] += 1
        if (list[i] == 512):
            res[2] += 1
        if (list[i] == 256):
            res[3] += 1
        if (list[i] == 128):
            res[4] += 1
        if (list[i] == 64):
            res[5] += 1
        if (list[i] == 32):
            res[6] += 1
        if (list[i] == 16):
            res[7] += 1
        if (list[i] == 8):
            res[8] += 1
        if (list[i] == 4):
            res[9] += 1
        if (list[i] == 2):
            res[10] += 1
    return res

def copy_field(field): # Копирование поля
    temp = [[],[],[],[]]
    for i in field[0]:
        temp[0].append(i)
    for i in field[1]:
        temp[1].append(i)
    for i in field[2]:
        temp[2].append(i)
    for i in field[3]:
        temp[3].append(i)
    return temp

def game_human(field): # Взаимодействие с игроком
    while (canMove(field) != [False, False, False, False]):  # Игра продолжается пока можно передвигаться
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
                can = canMove(field)
                if ((event.key == pygame.K_LEFT) and can[0]):
                    field = moveLeft(field)
                    insertNumber(field, generateListEmpty(field))
                if ((event.key == pygame.K_RIGHT) and can[1]):
                    field = moveRight(field)
                    insertNumber(field, generateListEmpty(field))
                if ((event.key == pygame.K_UP) and can[2]):
                    field = moveUp(field)
                    insertNumber(field, generateListEmpty(field))
                if ((event.key == pygame.K_DOWN) and can[3]):
                    field = moveDown(field)
                    insertNumber(field, generateListEmpty(field))
                drawInterface()  # Обновление игры
                pygame.display.update()

def game_bot2(field): # ИИ, расчитывающий действия на 2 хода вперед
    while ((field[0][0] == 0) or (field[0][1] == 0) or (field[0][2] == 0) or (field[0][3] == 0) or field[0][3] < 4):
        #time.sleep(0.5)
        can = canMove(field)
        if (can[2]):
            field = moveUp(field)
            insertNumber(field, generateListEmpty(field))
            drawInterface()  # Обновление игры
            pygame.display.update()
        if (can[0]):
            field = moveLeft(field)
            insertNumber(field, generateListEmpty(field))
            drawInterface()
            pygame.display.update()
        if not(can[0] or can[2]):
            break

    while (canMove(field) != [False, False, False, False]):  # Игра продолжается пока можно передвигаться
#                             Лево   Право  Верх   Низ
        #time.sleep(0.5)
        can = canMove(field)
        case_l = copy_field(field)
        case_r = copy_field(field)
        case_u = copy_field(field)
        if not ((can[0] == False) and (can[1] == False) and (can[2] == False)): # Если можно сдвинуться куда-либо кроме низа
            if can[0]: # Заполняем ситуации 1 хода
                case_l = moveLeft(case_l)
            else:
                case_l = 0
            if can[1]:
                case_r = moveRight(case_r)
            else:
                case_r = 0
            if can[2]:
                case_u = moveUp(case_u)
            else:
                case_u = 0

            if (case_l != 0): # Создаем копии 2 хода
                can_l = canMove(case_l)
                case_ll = copy_field(case_l)
                case_lr = copy_field(case_l)
                case_lu = copy_field(case_l)
            else:
                can_l = [False, False, False, False]
                case_ll = 0
                case_lr = 0
                case_lu = 0
            if (case_r != 0):
                can_r = canMove(case_r)
                case_rl = copy_field(case_r)
                case_rr = copy_field(case_r)
                case_ru = copy_field(case_r)
            else:
                can_r = [False, False, False, False]
                case_rl = 0
                case_rr = 0
                case_ru = 0
            if (case_u != 0):
                can_u = canMove(case_u)
                case_ul = copy_field(case_u)
                case_ur = copy_field(case_u)
                case_uu = copy_field(case_u)
            else:
                can_u = [False, False, False, False]
                case_ul = 0
                case_ur = 0
                case_uu = 0

            if can_l[0]: # Заполняем ситуации 2 хода l
                case_ll = moveLeft(case_ll)
            else:
                case_ll = 0
            if can_l[1]:
                case_lr = moveRight(case_lr)
            else:
                case_lr = 0
            if can_l[2]:
                case_lu = moveUp(case_lu)
            else:
                case_lu = 0
            if can_r[0]: # Заполняем ситуации 2 хода r
                case_rl = moveLeft(case_rl)
            else:
                case_rl = 0
            if can_r[1]:
                case_rr = moveRight(case_rr)
            else:
                case_rr = 0
            if can_r[2]:
                case_ru = moveUp(case_ru)
            else:
                case_ru = 0
            if can_u[0]: # Заполняем ситуации 2 хода u
                case_ul = moveLeft(case_ul)
            else:
                case_ul = 0
            if can_u[1]:
                case_ur = moveRight(case_ur)
            else:
                case_ur = 0
            if can_u[2]:
                case_uu = moveUp(case_uu)
            else:
                case_uu = 0

            if (case_ll != 0): # Рассчитываем силу каждой ситуации 2 хода l
                strength_ll = count_numbers(case_ll)
            if (case_lr != 0):
                strength_lr = count_numbers(case_lr)
            if (case_lu != 0):
                strength_lu = count_numbers(case_lu)
            if (case_rl != 0): # Рассчитываем силу каждой ситуации 2 хода r
                strength_rl = count_numbers(case_rl)
            if (case_rr != 0):
                strength_rr = count_numbers(case_rr)
            if (case_ru != 0):
                strength_ru = count_numbers(case_ru)
            if (case_ul != 0): # Рассчитываем силу каждой ситуации 2 хода u
                strength_ul = count_numbers(case_ul)
            if (case_ur != 0):
                strength_ur = count_numbers(case_ur)
            if (case_uu != 0):
                strength_uu = count_numbers(case_uu)

            if (case_ll == 0): # Заполняем нулевые l
                strength_ll = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_lr == 0):
                strength_lr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_lu == 0):
                strength_lu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_rl == 0): # Заполняем нулевые r
                strength_rl = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_rr == 0):
                strength_rr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_ru == 0):
                strength_ru = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_ul == 0): # Заполняем нулевые u
                strength_ul = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_ur == 0):
                strength_ur = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if (case_uu == 0):
                strength_uu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            i = -1 # Ищем лучший ход
            best = "much"
            while ((best == "much") and i != 10):
                i += 1
                if ((strength_ll[i] > strength_lr[i]) and (strength_ll[i] > strength_lu[i]) and (strength_ll[i] > strength_rl[i]) and (strength_ll[i] > strength_rr[i]) and (strength_ll[i] > strength_ru[i]) and (strength_ll[i] > strength_ul[i]) and (strength_ll[i] > strength_ur[i]) and (strength_ll[i] > strength_uu[i])):
                    best = "left"
                if ((strength_lr[i] > strength_ll[i]) and (strength_lr[i] > strength_lu[i]) and (strength_lr[i] > strength_rl[i]) and (strength_lr[i] > strength_rr[i]) and (strength_lr[i] > strength_ru[i]) and (strength_lr[i] > strength_ul[i]) and (strength_lr[i] > strength_ur[i]) and (strength_lr[i] > strength_uu[i])):
                    best = "left"
                if ((strength_lu[i] > strength_lr[i]) and (strength_lu[i] > strength_ll[i]) and (strength_lu[i] > strength_rl[i]) and (strength_lu[i] > strength_rr[i]) and (strength_lu[i] > strength_ru[i]) and (strength_lu[i] > strength_ul[i]) and (strength_lu[i] > strength_ur[i]) and (strength_lu[i] > strength_uu[i])):
                    best = "left"
                if ((strength_rl[i] > strength_lr[i]) and (strength_rl[i] > strength_lu[i]) and (strength_rl[i] > strength_ll[i]) and (strength_rl[i] > strength_rr[i]) and (strength_rl[i] > strength_ru[i]) and (strength_rl[i] > strength_ul[i]) and (strength_rl[i] > strength_ur[i]) and (strength_rl[i] > strength_uu[i])):
                    best = "right"
                if ((strength_rr[i] > strength_ll[i]) and (strength_rr[i] > strength_lu[i]) and (strength_rr[i] > strength_rl[i]) and (strength_rr[i] > strength_lr[i]) and (strength_rr[i] > strength_ru[i]) and (strength_rr[i] > strength_ul[i]) and (strength_rr[i] > strength_ur[i]) and (strength_rr[i] > strength_uu[i])):
                    best = "right"
                if ((strength_ru[i] > strength_lr[i]) and (strength_ru[i] > strength_ll[i]) and (strength_ru[i] > strength_rl[i]) and (strength_ru[i] > strength_rr[i]) and (strength_ru[i] > strength_lu[i]) and (strength_ru[i] > strength_ul[i]) and (strength_ru[i] > strength_ur[i]) and (strength_ru[i] > strength_uu[i])):
                    best = "right"
                if ((strength_ul[i] > strength_lr[i]) and (strength_ul[i] > strength_lu[i]) and (strength_ul[i] > strength_ll[i]) and (strength_ul[i] > strength_rr[i]) and (strength_ul[i] > strength_ru[i]) and (strength_ul[i] > strength_rl[i]) and (strength_ul[i] > strength_ur[i]) and (strength_ul[i] > strength_uu[i])):
                    best = "up"
                if ((strength_ur[i] > strength_ll[i]) and (strength_ur[i] > strength_lu[i]) and (strength_ur[i] > strength_rl[i]) and (strength_ur[i] > strength_lr[i]) and (strength_ur[i] > strength_ru[i]) and (strength_ur[i] > strength_ul[i]) and (strength_ur[i] > strength_rr[i]) and (strength_ur[i] > strength_uu[i])):
                    best = "up"
                if ((strength_uu[i] > strength_lr[i]) and (strength_uu[i] > strength_ll[i]) and (strength_uu[i] > strength_rl[i]) and (strength_uu[i] > strength_rr[i]) and (strength_uu[i] > strength_lu[i]) and (strength_uu[i] > strength_ul[i]) and (strength_uu[i] > strength_ur[i]) and (strength_uu[i] > strength_ru[i])):
                    best = "up"

            if ((best == "much") and (case_u != 0)): # Ходим
                field = moveUp(field)
                insertNumber(field, generateListEmpty(field))
            elif ((best == "much") and (case_l != 0)):
                field = moveLeft(field)
                insertNumber(field, generateListEmpty(field))
            elif ((best == "much") and (case_r != 0)):
                field = moveRight(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "up"):
                field = moveUp(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "left"):
                field = moveLeft(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "right"):
                field = moveRight(field)
                insertNumber(field, generateListEmpty(field))
        else:
            field = moveDown(field)
            insertNumber(field, generateListEmpty(field))

        drawInterface()  # Обновление игры
        pygame.display.update()

def game_bot2_new(field): # ИИ, расчитывающий действия на 2 хода вперед
    while (canMove(field) != [False, False, False, False]):  # Игра продолжается пока можно передвигаться
#                             Лево   Право  Верх   Низ
        #time.sleep(0.5)
        can = canMove(field)
        case_l = copy_field(field)
        case_r = copy_field(field)
        case_u = copy_field(field)
        if not ((can[0] == False) and (can[1] == False) and (can[2] == False)): # Если можно сдвинуться куда-либо кроме низа
            if can[0]: # Заполняем ситуации 1 хода
                case_l = moveLeft(case_l)
            else:
                case_l = 0
            if can[1]:
                case_r = moveRight(case_r)
            else:
                case_r = 0
            if can[2]:
                case_u = moveUp(case_u)
            else:
                case_u = 0

            if (case_l != 0): # Создаем копии 2 хода
                can_l = canMove(case_l)
                case_ll = copy_field(case_l)
                case_lr = copy_field(case_l)
                case_lu = copy_field(case_l)
            else:
                can_l = [False, False, False, False]
                case_ll = 0
                case_lr = 0
                case_lu = 0
            if (case_r != 0):
                can_r = canMove(case_r)
                case_rl = copy_field(case_r)
                case_rr = copy_field(case_r)
                case_ru = copy_field(case_r)
            else:
                can_r = [False, False, False, False]
                case_rl = 0
                case_rr = 0
                case_ru = 0
            if (case_u != 0):
                can_u = canMove(case_u)
                case_ul = copy_field(case_u)
                case_ur = copy_field(case_u)
                case_uu = copy_field(case_u)
            else:
                can_u = [False, False, False, False]
                case_ul = 0
                case_ur = 0
                case_uu = 0

            if can_l[0]: # Заполняем ситуации 2 хода l
                case_ll = moveLeft(case_ll)
                case_ll = getComputerWay(case_ll)
            else:
                case_ll = 0
            if can_l[1]:
                case_lr = moveRight(case_lr)
                case_lr = getComputerWay(case_lr)
            else:
                case_lr = 0
            if can_l[2]:
                case_lu = moveUp(case_lu)
                case_lu = getComputerWay(case_lu)
            else:
                case_lu = 0
            if can_r[0]: # Заполняем ситуации 2 хода r
                case_rl = moveLeft(case_rl)
                case_rl = getComputerWay(case_rl)
            else:
                case_rl = 0
            if can_r[1]:
                case_rr = moveRight(case_rr)
                case_rr = getComputerWay(case_rr)
            else:
                case_rr = 0
            if can_r[2]:
                case_ru = moveUp(case_ru)
                case_ru = getComputerWay(case_ru)
            else:
                case_ru = 0
            if can_u[0]: # Заполняем ситуации 2 хода u
                case_ul = moveLeft(case_ul)
                case_ul = getComputerWay(case_ul)
            else:
                case_ul = 0
            if can_u[1]:
                case_ur = moveRight(case_ur)
                case_ur = getComputerWay(case_ur)
            else:
                case_ur = 0
            if can_u[2]:
                case_uu = moveUp(case_uu)
                case_uu = getComputerWay(case_uu)
            else:
                case_uu = 0

            if (case_ll != 0): # Рассчитываем силу каждой ситуации 2 хода l
                strength_ll = 0
                for way in case_ll:
                    strength_ll += getStrength(field, way)
                strength_ll /= (emptyCount(case_ll[0]) + 1)
            if (case_lr != 0):
                strength_lr = 0
                for way in case_lr:
                    strength_lr += getStrength(field, way)
                strength_lr /= (emptyCount(case_lr[0]) + 1)
            if (case_lu != 0):
                strength_lu = 0
                for way in case_lu:
                    strength_lu += getStrength(field, way)
                strength_lu /= (emptyCount(case_lu[0]) + 1)
            if (case_rl != 0): # Рассчитываем силу каждой ситуации 2 хода r
                strength_rl = 0
                for way in case_rl:
                    strength_rl += getStrength(field, way)
                strength_rl /= (emptyCount(case_rl[0]) + 1)
            if (case_rr != 0):
                strength_rr = 0
                for way in case_rr:
                    strength_rr += getStrength(field, way)
                strength_rr /= (emptyCount(case_rr[0]) + 1)
            if (case_ru != 0):
                strength_ru = 0
                for way in case_ru:
                    strength_ru += getStrength(field, way)
                strength_ru /= (emptyCount(case_ru[0]) + 1)
            if (case_ul != 0): # Рассчитываем силу каждой ситуации 2 хода u
                strength_ul = 0
                for way in case_ul:
                    strength_ul += getStrength(field, way)
                strength_ul /= (emptyCount(case_ul[0]) + 1)
            if (case_ur != 0):
                strength_ur = 0
                for way in case_ur:
                    strength_ur += getStrength(field, way)
                strength_ur /= (emptyCount(case_ur[0]) + 1)
            if (case_uu != 0):
                strength_uu = 0
                for way in case_uu:
                    strength_uu += getStrength(field, way)
                strength_uu /= (emptyCount(case_uu[0]) + 1)

            if (case_ll == 0): # Заполняем нулевые l
                strength_ll = 0
            if (case_lr == 0):
                strength_lr = 0
            if (case_lu == 0):
                strength_lu = 0
            if (case_rl == 0): # Заполняем нулевые r
                strength_rl = 0
            if (case_rr == 0):
                strength_rr = 0
            if (case_ru == 0):
                strength_ru = 0
            if (case_ul == 0): # Заполняем нулевые u
                strength_ul = 0
            if (case_ur == 0):
                strength_ur = 0
            if (case_uu == 0):
                strength_uu = 0

            i = -1 # Ищем лучший ход
            best = "much"
            while ((best == "much") and i != 10):
                i += 1
                if ((strength_ll > strength_lr) and (strength_ll > strength_lu) and (
                        strength_ll > strength_rl) and (strength_ll > strength_rr) and (
                        strength_ll > strength_ru) and (strength_ll > strength_ul) and (
                        strength_ll > strength_ur) and (strength_ll > strength_uu)):
                    best = "left"
                if ((strength_lr > strength_ll) and (strength_lr > strength_lu) and (
                        strength_lr > strength_rl) and (strength_lr > strength_rr) and (
                        strength_lr > strength_ru) and (strength_lr > strength_ul) and (
                        strength_lr > strength_ur) and (strength_lr > strength_uu)):
                    best = "left"
                if ((strength_lu > strength_lr) and (strength_lu > strength_ll) and (
                        strength_lu > strength_rl) and (strength_lu > strength_rr) and (
                        strength_lu > strength_ru) and (strength_lu > strength_ul) and (
                        strength_lu > strength_ur) and (strength_lu > strength_uu)):
                    best = "left"
                if ((strength_rl > strength_lr) and (strength_rl > strength_lu) and (
                        strength_rl > strength_ll) and (strength_rl > strength_rr) and (
                        strength_rl > strength_ru) and (strength_rl > strength_ul) and (
                        strength_rl > strength_ur) and (strength_rl > strength_uu)):
                    best = "right"
                if ((strength_rr > strength_ll) and (strength_rr > strength_lu) and (
                        strength_rr > strength_rl) and (strength_rr > strength_lr) and (
                        strength_rr > strength_ru) and (strength_rr > strength_ul) and (
                        strength_rr > strength_ur) and (strength_rr > strength_uu)):
                    best = "right"
                if ((strength_ru > strength_lr) and (strength_ru > strength_ll) and (
                        strength_ru > strength_rl) and (strength_ru > strength_rr) and (
                        strength_ru > strength_lu) and (strength_ru > strength_ul) and (
                        strength_ru > strength_ur) and (strength_ru > strength_uu)):
                    best = "right"
                if ((strength_ul > strength_lr) and (strength_ul > strength_lu) and (
                        strength_ul > strength_ll) and (strength_ul > strength_rr) and (
                        strength_ul > strength_ru) and (strength_ul > strength_rl) and (
                        strength_ul > strength_ur) and (strength_ul > strength_uu)):
                    best = "up"
                if ((strength_ur > strength_ll) and (strength_ur > strength_lu) and (
                        strength_ur > strength_rl) and (strength_ur > strength_lr) and (
                        strength_ur > strength_ru) and (strength_ur > strength_ul) and (
                        strength_ur > strength_rr) and (strength_ur > strength_uu)):
                    best = "up"
                if ((strength_uu > strength_lr) and (strength_uu > strength_ll) and (
                        strength_uu > strength_rl) and (strength_uu > strength_rr) and (
                        strength_uu > strength_lu) and (strength_uu > strength_ul) and (
                        strength_uu > strength_ur) and (strength_uu > strength_ru)):
                    best = "up"

            if ((best == "much") and (case_u != 0)): # Ходим
                field = moveUp(field)
                insertNumber(field, generateListEmpty(field))
            elif ((best == "much") and (case_l != 0)):
                field = moveLeft(field)
                insertNumber(field, generateListEmpty(field))
            elif ((best == "much") and (case_r != 0)):
                field = moveRight(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "up"):
                field = moveUp(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "left"):
                field = moveLeft(field)
                insertNumber(field, generateListEmpty(field))
            if (best == "right"):
                field = moveRight(field)
                insertNumber(field, generateListEmpty(field))
        else:
            field = moveDown(field)
            insertNumber(field, generateListEmpty(field))

        drawInterface()  # Обновление игры
        pygame.display.update()

def coordNew(field_old, field_new):
    for i in range(4):
        for j in range(4):
            if (field_old[i][j] != field_new[i][j]):
                return [i, j]

def getStrength(field_old, field_new):
    smoothness_new = monotonicity(field_new)
    monotonicity_new = monotonicity(field_new)
    empty_count_new = emptyCount(field_new)
    max_value_new = highest(field_new)
    smoothness_old = monotonicity(field_old)
    monotonicity_old = monotonicity(field_old)
    empty_count_old = emptyCount(field_old)
    max_value_old = highest(field_old)
    if (smoothness_old != 0):
        q_smooth = smoothness_new/smoothness_old
    else:
        q_smooth = 0
    if (monotonicity_old != 0):
        q_monot = monotonicity_new/monotonicity_old
    else:
        q_monot = 0
    if (empty_count_old != 0):
        q_empty = empty_count_new/empty_count_old
    else:
        q_empty = 0
    if (max_value_old != 0):
        q_maxval = max_value_new/max_value_old
    else:
        q_maxval = 0
    smooth_weight = 0.1
    monot_weight = 1
    empty_weight = 3
    maxval_weight = 1
    res = (q_smooth * smooth_weight) + (q_monot * monot_weight) + (q_empty * empty_weight) + (q_maxval * maxval_weight)
    return res

def getComputerWay(field):
    copy2 = copy_field(field)
    copy4 = copy_field(field)
    res = []
    for i in range(4):
        for j in range(4):
            if (field[i][j] == 0):
                copy2[i][j] = 2
                res.append(copy2)
                copy4[i][j] = 4
                res.append(copy4)
                copy2 = copy_field(field)
                copy4 = copy_field(field)

    return res


COLORS = { # Цветовые константы
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 128, 255),
    16: (128, 255, 255),
    32: (255, 255, 0),
    64: (255, 0, 255),
    128: (0, 255, 255),
    256: (128, 128, 0),
    512: (128, 0, 128),
    1024: (0, 128, 128),
    2048: (64, 255, 0)
}
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)

BLOCKS = 4 # Константы размеров
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110

pygame.init() # Запуск pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)

# main

field = generateField() # Начальная генерация
i = randint(0, 3)
j = randint(0, 3)
field[i][j] = 2

drawInterface() # Сама игра
pygame.display.update()
game_bot2_new(field) # Можно заменить на game_human(field) и играть самому

exp = [] # Тестирование большим количеством симуляций
n = 100
for i in range(n):
    field = generateField()
    i = randint(0, 3)
    j = randint(0, 3)
    field[i][j] = 2
    drawInterface()
    pygame.display.update()
    game_bot2(field)
    exp.append(highest(field))

list = count_exp(exp) # Вывод результатов теста
num = 2048
for i in list:
    print(str(num)+" - "+str(i))
    num //= 2

field = generateField() # Окно GameOver
drawInterface()
font = pygame.font.SysFont("stxingkai", 100)
text = font.render(f'{"Game Over"}', True, WHITE)
text_x = 60
text_y = 320
screen.blit(text, (text_x, text_y))
pygame.display.update()
time.sleep(10)