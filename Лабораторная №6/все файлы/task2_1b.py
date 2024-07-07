#!/usr/bin/env python3
from ev3dev.ev3 import LargeMotor
from ev3dev2.power import PowerSupply
import time
import os
import shutil

# Класс для получения данных о заряде батареи
volts = PowerSupply()
# Класс для взаимодействия с двигателем
motorA = LargeMotor('outA')

# Создаем папочку для данных
k_p = 50#!!!!!!!нужно для трех разных k снять, меняем к - > меняем в названии файла значение k
theta_max = 0

file = '/home/robot/task2.1b/task2.1b_k_p=50'
f=open(file, "a")
try:
     # Сохраняем начальное время
    start_time = time.time()
    # Сохраняем начальную позицию
    motorA.position=0
    # В течение двух секунд записываем в файл данные в формате: <time,angle>
    while (time.time() - start_time) < 5:
        theta = motorA.position
        # Подаем на мотор напряжение U
        g=time.time()
        error = g - theta
        U = k_p * error
        if U>100:
            U=100
        if U<-100:
            U=-100
        motorA.run_direct(duty_cycle_sp=U)
        if motorA.position > theta_max:
            theta_max = motorA.position
            # Конструкция 'with open() as f' означает то же самое, что и 'f = open(); ...; f.close()'
            print(str(time.time() - start_time) + ',' + str(theta))
            f.write(str(time.time() - start_time) + ',' + str(theta) + '\n')
    f.write("\nError is" + str(error))
    # Останавливаем мотор
    motorA.run_direct(duty_cycle_sp=0)
    time.sleep(1)
except Exception as e:
    raise e
finally:
    # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')

# Выводим заряд батареи, то есть реальное напряжение в вольтах, которое подается на двигатель при 100% поданной на него мощности
print("Volts: " + str(volts.measured_volts))

