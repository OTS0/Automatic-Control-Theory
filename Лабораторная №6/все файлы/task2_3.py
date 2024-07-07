#!/usr/bin/env python3
from ev3dev.ev3 import LargeMotor
from ev3dev2.power import PowerSupply
import time
import os
import shutil
import math
# Класс для получения данных о заряде батареи
volts = PowerSupply()
# Класс для взаимодействия с двигателем
motorA = LargeMotor('outA')

# Создаем папочку для данных
file='/home/robot/task2.3/2.3_last'
f=open(file,"a")
k_p = 5#!!!!!!!нужно для трех разных k снять, меняем к - > меняем в названии файла значение k
k_i=0.005
theta_max = 0
error_last_1=0
error_last_2=0
error_last_3=0
u_last_1 = 0
u_last_2=0
u_last_3=0
try:
     # Сохраняем начальное время
    start_time = time.time()
    # Сохраняем начальную позицию
    motorA.position=0
    # В течение двух секунд записываем в файл данные в формате: <time,angle>
    while (time.time() - start_time) < 10:
        theta = motorA.position
        # Подаем на мотор напряжение U
        t=time.time()
        g=3*math.sin(motorA.speed*t+1)+2*math.cos(motorA.speed*t)
        er = g - theta
        delta_t =time.time()-t

        D =1/delta_t**3 - 5/delta_t**2 + 1/delta_t - 5
        A=(3*u_last_1 - 3*u_last_2 + u_last_3)/(delta_t**3*D)
        B=5*(-2*u_last_1+u_last_2)/(D*(delta_t**2))
        C=u_last_1/(delta_t*D)

        E1=2.95*(er-3*error_last_1 + 3 * error_last_2 - error_last_3)/delta_t**3
        E2=0.25*(er-2*error_last_1 + error_last_2)/delta_t**2
        E3=2.75*(er-error_last_1)/delta_t
        E=E1+E2+E3+0.05*er
        U = A+B+C+E/D
        if U>100:
            U=100
        if U<-100:
            U=-100
        motorA.run_direct(duty_cycle_sp=U)
        error_last_1 = er
        error_last_2 = error_last_1
        error_last_3 = error_last_2
        u_last_1 = U
        u_last_2 = u_last_1
        u_last_3 = u_last_2
        t_last=time.time
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

