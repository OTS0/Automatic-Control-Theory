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

os.makedirs('/home/robot/task2.2b')#cоздание папки
file = '/home/robot/task2.2b/task2.2b_k_p=' + k_p
f=open(file, "a")
k_p = 0.5 #!!!!!!!нужно для трех разных k снять, меняем к - > меняем в названии файла значение k
k_i=0.5
start_pos = motorA.position
d = 3.14
error = d - start_pos
try:
     # Сохраняем начальное время
    start_time = time.time()
    # Сохраняем начальную позицию
    motorA.position=0
    # В течение двух секунд записываем в файл данные в формате: <time,angle>
    while (time.time() - start_time) < 10:
        theta = motorA.position
        i+= k_i * error * (time.time() - t)
        t=time.time()
        U = k_p * error + i
        error_last = error
        if U>100:
            U=100
        if U<-100:
            U=-100
        motorA.run_direct(duty_cycle_sp=U)
        error = d - math.radians(motorA.position)
        d += (time.time() - start_time)
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