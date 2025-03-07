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
if os.path.exists('/home/robot/data_4'):
    shutil.rmtree('/home/robot/data_4')

os.makedirs('/home/robot/data_4')

try:
    Um = volts.measured_volts
    motorA.position = 0
    start_pos = motorA.position
    dest = 3.14
    kP = 3
    start_time = time.time()
    error = dest - motorA.position

    #to reset
    delay = 0.07

    while(time.time() - start_time < 10):

        if kP*error > Um:
            U = 100
        elif kP*error < -Um:
            U = -100
        else:
            U = kP*error / Um * 100                 #U = kP * e^(tau)?

        motorA.run_direct(duty_cycle_sp=U)

        # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
        with open('data_4/'+'delay=' + str(delay), "a") as f:
            print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
            f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')

        error = dest - math.radians(motorA.position)
        time.sleep(delay)

except Exception as e:
    raise e

finally:
  # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')