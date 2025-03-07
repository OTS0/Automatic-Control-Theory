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
if os.path.exists('/home/robot/data_2_3'):
    shutil.rmtree('/home/robot/data_2_3')

os.makedirs('/home/robot/data_2_3')

try: 
  start_time = time.time()
  motorA.position = 0
  start_pos = motorA.position
  prev_time = start_time
  U_prev = U_pprev = e_prev = e_pprev = 0
  Umax = volts.measured_volts
  k0 = 0.16
  k1 = 0.64
  k2 = 0.96

  while(time.time() - start_time < 20):

    dest_pos = math.sin((time.time()-start_time) + math.pi) *180/math.pi
    error = dest_pos - motorA.position

    dt = (time.time() - prev_time)
    prev_time = time.time()

    #U = (1.92*U_prev-0.96*U_pprev+0.64*dt*U_prev)/(0.16*dt*dt+0.64*dt+0.96)+((1+dt*dt)*error-2*e_prev+e_pprev)/(0.16*dt*dt+0.64*dt+0.96)
    xd = 0.96/dt/dt+0.64/dt+0.16
    U = (2*k2*U_prev-k2*U_pprev)/(dt*dt*xd)+(k1*U_prev)/(dt*xd)+(error-2*e_prev+e_pprev)/(dt*dt*xd)+error
    print('U = '+str(U)+'\n')

    

    if U > 100:
      U = 100
    elif U < -100:
      U = -100

    motorA.run_direct(duty_cycle_sp=U)

    U_pprev = U_prev
    U_prev = U
    e_pprev = e_prev
    e_prev = error

    

    # В течение 10 секунд записываем в файл данные в формате: <time,angle,speed,error>
    with open('data_2_3/'+'special_reg', "a") as f:
      print(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error))
      f.write(str(time.time() - start_time) + ',' + str(motorA.position - start_pos) + ',' + str(motorA.speed) + ',' + str(error) + '\n')
    
  #motorA.run_direct(duty_cycle_sp=0)
  #time.sleep(1)

except Exception as e:
    raise e

finally:
  # Останавливаем мотор в случае ошибок в коде
    motorA.stop(stop_action='brake')