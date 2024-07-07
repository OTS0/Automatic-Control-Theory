#!/usr/bin/env python3
import math
import time

from ev3dev.ev3 import LargeMotor
import os
import shutil

A1 = 80
A2 = 20
A3 = 70
w1 = 10
w2 = 20
w3 = 8

# Класс для взаимодействия с двигателем
motorA = LargeMotor('outA')

# Создаем папочку для данных
name_dir = '/home/robot/results_sincos'
if os.path.exists(name_dir):
    shutil.rmtree(name_dir)

os.makedirs(name_dir)

try:
    # Сохраняем начальное время
    start_time = time.time()
    # Задаем начальное входное напряжение, которое будет меняться от 20% до 100% с шагом 20
    U = 0
    # Сохраняем начальную позицию
    start_pos = motorA.position
    # Название файла
    name_file = name_dir + '/sincos'

    # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed>
    t = time.time() - start_time
    while t < 2:
        U = A2 * math.sin(w2 * t) + A3 * math.cos(w3 * t)
        # Подаем на мотор напряжение U
        motorA.run_direct(duty_cycle_sp=U)

        # Конструкция 'with open() as f' означает то же самое, что и 'f = open(); ...; f.close()'
        with open(name_file, "a") as f:
            f.write(
                str(str(t) + ',' + str(U) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + '\n'))

        t = time.time() - start_time
except Exception as e:
    raise e
finally:
    # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')
