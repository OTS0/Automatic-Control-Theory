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
if os.path.exists('/home/robot/task2.3'):#проверяет есть ли такой путь
    shutil.rmtree('/home/robot/task2.3') #удаление папки

os.makedirs('/home/robot/task2.3')#cоздание папки
error_last_1=0
error_last_2=0
error_last_3=0
u_last_1 = 0
u_last_2=0
u_last_3=0
t=0
d=0
er=0
delta_t=0
D=0
A=0
B=0
C=0
E1=0
E2=0
E=0
E3=0
U=0
theta=0
motorA.position = 0
start_pos = motorA.position
prev_time = start_time
U_prev = U_pprev = e_prev = e_pprev = 0
Umax = volts.measured_volts
try:
     # Сохраняем начальное время
    start_time = time.time()
    # Сохраняем начальную позицию
    motorA.position=0
    # В течение двух секунд записываем в файл данные в формате: <time,angle>
    f=open('/home/robot/task2.3/task2_3', "a")
    while (time.time() - start_time) < 50:
        # Подаем на мотор напряжение U
        t=time.time()
        d = 3 * math.sin(time.time()-start_time) + 2 * math.cos(time.time()-start_time)*180/math.pi
        er = d - theta
        delta_t =time.time()-start_time

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
