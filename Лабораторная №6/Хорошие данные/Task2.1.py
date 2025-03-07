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
if os.path.exists('/home/robot/data_2_1'):
    shutil.rmtree('/home/robot/data_2_1')

os.makedirs('/home/robot/data_2_1')


#CONSTANT KP
for i in range(3):
  try:

    Umax = volts.measured_volts
    kP = (1+i) * 3
    start_time = time.time()
    start_pos = 0
    motorA.position = 0
    dest_pos = 6.28
    error = dest_pos

    while(time.time() - start_time < 10):

      U = kP * error
      if U/Umax > 1:
        U = 100
      elif U/Umax < -1:
        U = -100
      else:
        U = U/Umax * 100
      motorA.run_direct(duty_cycle_sp = U)

      #В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
      with open('data_2_1/'+str(kP)+'_constant', "a") as f:
        print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
        f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')

      error = dest_pos - math.radians(motorA.position)

    motorA.run_direct(duty_cycle_sp=0)
    time.sleep(1)


  except Exception as e:
     raise e

  finally:
    # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')


#LINEAR KP
for i in range(3):
  try:
    Umax = volts.measured_volts
    kP = (1+i) * 3
    start_time = time.time()
    start_pos = 0
    motorA.position = 0
    dest_pos = 6.28
    error = dest_pos

    while(time.time() - start_time < 10):
      
      U = kP * error
      if U/Umax > 1:
        U = 100
      elif U/Umax < -1:
        U = -100
      else:
        U = U/Umax*100
      motorA.run_direct(duty_cycle_sp=U)

      error = dest_pos - math.radians(motorA.position)
      # линейно возрастает
      dest_pos = 6.28 + (time.time() - start_time) 

       # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
      with open('data_2_1/'+str(kP)+'_linear', "a") as f:
        print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
        f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')
    motorA.run_direct(duty_cycle_sp=0)
  
    time.sleep(1)

  except Exception as e:
      raise e

  finally:
    # Останавливаем мотор в случае ошибок в коде
      motorA.stop(stop_action='brake')
