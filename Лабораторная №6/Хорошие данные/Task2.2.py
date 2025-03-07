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
if os.path.exists('/home/robot/data_2_2'):
    shutil.rmtree('/home/robot/data_2_2')

os.makedirs('/home/robot/data_2_2')

try:
  kP = 1
  kI = 1
  Umax = volts.measured_volts
  start_time = time.time()
  motorA.position = 0
  start_pos = motorA.position
  dest_pos = 6.28 ##in rads
  error = dest_pos - start_pos
  t_prev = start_time
  I = P = 0

  while(time.time() - start_time < 10):
    P = kP * error
    I += kI * error * (time.time() - t_prev)
    t_prev = time.time()
    U = P + I
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
    with open('data_2_2/'+str(kI)+'_linear', "a") as f:
      print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
      f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')

  motorA.run_direct(duty_cycle_sp=0)
  time.sleep(1)

except Exception as e:
    raise e

finally:
  # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')




try:
  kP = 1
  kI = 1
  Umax = volts.measured_volts
  start_time = time.time()
  motorA.position = 0
  start_pos = motorA.position
  dest_pos = 6.28 ##in rads
  error = dest_pos - start_pos
  t_prev = start_time
  I = P = 0

  while(time.time() - start_time < 10):
    P = kP * error
    I += kI * error * (time.time() - t_prev)
    t_prev = time.time()
    U = P + I
    if U/Umax > 1:
      U = 100
    elif U/Umax < -1:
      U = -100
    else:
      U = U/Umax*100 
    motorA.run_direct(duty_cycle_sp=U)

    error = dest_pos - math.radians(motorA.position)
    # линейно возрастает
    dest_pos = 6.28 + (time.time() - start_time)**2
    # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
    with open('data_2_2/'+str(kI)+'_squared', "a") as f:
      print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
      f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')

  motorA.run_direct(duty_cycle_sp=0)
  time.sleep(1)

except Exception as e:
    raise e

finally:
  # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')


try:
  kP = 1
  kI = 1
  Umax = volts.measured_volts
  start_time = time.time()
  motorA.position = 0
  start_pos = motorA.position
  dest_pos = 6.28 ##in rads
  error = dest_pos - start_pos
  t_prev = start_time
  I = P = 0

  while(time.time() - start_time < 10):
    P = kP * error
    I += kI * error * (time.time() - t_prev)
    t_prev = time.time()
    U = P + I
    if U/Umax > 1:
      U = 100
    elif U/Umax < -1:
      U = -100
    else:
      U = U/Umax*100 
    motorA.run_direct(duty_cycle_sp=U)

    error = dest_pos - math.radians(motorA.position)
    # линейно возрастает
    dest_pos = 6.28 + (time.time() - start_time)**3
    # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
    with open('data_2_2/'+str(kI)+'_cubic', "a") as f:
      print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
      f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')

  motorA.run_direct(duty_cycle_sp=0)
  time.sleep(1)

except Exception as e:
    raise e

finally:
  # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')