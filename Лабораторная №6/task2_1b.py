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
if os.path.exists('/home/robot/task2.1b'):#проверяет есть ли такой путь
    shutil.rmtree('/home/robot/task2.1b') #удаление папки

os.makedirs('/home/robot/task2.1b')#cоздание папки
k_p = 1#!!!!!!!нужно для трех разных k снять, меняем к - > меняем в названии файла значение k
start_pos = motorA.position
file = '/home/robot/task2.1b/task2.1b_k_p='+ k_p
f=open(file, "a")
d = 6.28
error = d - start_pos
try:
     # Сохраняем начальное время
    start_time = time.time()
    # Сохраняем начальную позицию
    motorA.position=0
    # В течение двух секунд записываем в файл данные в формате: <time,angle>
    while (time.time() - start_time) < 10:
        theta = motorA.position
        # Подаем на мотор напряжение U
        U = k_p * error
        if U>100:
            U=100
        if U<-100:
            U=-100
        motorA.run_direct(duty_cycle_sp=U)
        error = d - math.radians(motorA.position)
        d = 6.28 + (time.time() - start_time)
        print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
        f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')
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

