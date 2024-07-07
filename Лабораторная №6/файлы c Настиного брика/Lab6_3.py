from ev3dev.ev3 import LargeMotor
from ev3dev2.power import PowerSupply
import types
from math import pi, sin, cos
import os
import shutil
import time

motor = LargeMotor('outA')
U_MAX = 6.8424
# матрица данных. Заранее создаю две нулевые строки для вычисления производных
data = [[0] * 6] * 2  # time, angle, speed, U, e, e_delay
# e - реальное отклонение от преследуемого сигнала
# e_delay - та ошибка которую видит сейчас регулятор и система (с запаздываением)
watching_var = "omega"  # theta or omega

# начальные характеристики системы
start_time = time.time()
angle = 0
speed = 0
start_angle = angle
start_speed = speed

# задержка
i = 1

# для АЧХ и ФЧХ изменяем её (при подаче на input_signal синуса с зависимостью от omega)
omega = 0
folder = ''
filename = ''

# Создаем папочку для данных
if os.path.exists('/home/robot/ex3'):
    shutil.rmtree('/home/robot/ex3')

os.makedirs('/home/robot/ex3')

# входной сигнал и регулятор. Их необходимо будет переопределить в коде. Ну или переписать здесь.
def input_signal(time):
    return 1

def regulator(e):
    return e

# основная функция. Здесь сигнал проходит путь от входа, до выхода и сохраняет состояние в данный момент времени в data
def movement():
    # время с начала запуска двигателя
    time_now = time.time() - start_time

    # т.к. система открытая, то считаем, что на входе у нас напряжение и просто считываем его
    U = input_signal(time_now)
    e = 0
    e_delay = 0

    U = U if abs(U) <= 100 else U / abs(U) * 100
    # добавляем данные в data
    data.append([time_now, motor.angle - start_angle, motor.speed - start_speed, U, e, e_delay])
    str_data = ",".join(list(map(str, self.data[-1])))
    with open(self.folder + '/' + self.filename, "a") as f:
        print(str_data)
        f.write(str_data + '\n')
    # подаём на моторчик необходимое напряжение
    motor.run_direct(duty_cycle_sp=U)

# остановка моторчика
def stop():
    motor.run_direct(duty_cycle_sp=0)


def sin_signal(time): # амлитуда и фаза входного сигнала
    A = 1 
    fi = pi/2
    return A * sin(omega * time_now + fi)

system_type = "open"
input_signal = types.MethodType(sin_signal, motor)

try:

    for omega1 in range(20):
        if os.path.exists('/home/robot/' + "ex3"):
            shutil.rmtree('/home/robot/' + "ex3")

        os.makedirs('/home/robot/' + "ex3")
        folder = "ex3"
        filename = "data_omega"
        print('save in /home/robot/' + "ex3" + '/' + "data_omega")
        # возвращение моторчика к исходному состоянию. Отчистка всех буфферов
        motor.stop(stop_action='brake')
        start_time = time.time()
        data = [[0] * 6] * 2
        start_angle = angle
        start_speed = speed
        i = 0
        time_now = 0

        omega = omega1  # устанавливаем некоторую частоту

        while time_now < 5:  # Запускаем моторчик и записываем данные с него в течение 5 секунд
            movement()
        stop()
        time.sleep(1)

except Exception as exception:
    raise exception
finally:
    # Останавливаем мотор в случае ошибок в коде
    stop()
