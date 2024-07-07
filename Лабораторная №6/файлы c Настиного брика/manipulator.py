#!/usr/bin/env python3
from ev3dev.ev3 import *
import time
from math import copysign, cos, sin, acos, asin, atan, atan2, pi



mA = LargeMotor("outA") # 1
mB = LargeMotor("outB") # 2
mC = LargeMotor("outC") # 3
ts1 = TouchSensor("in4")
ts2 = TouchSensor("in1")

theta1_d = 90
theta2_d = -90
theta3_d = 90

mA.position = 0  # 1 РјРѕС‚РѕСЂ
mB.position = 0  # 2 ldbufntkm
mC.position = 0

sum_e1= 0
sum_e2 = 0
sum_e3 = 0

Kp1 = 3
Ki1 = 0
Kd1 = 0.05

Kp2 = 3
Ki2 = 0
Kd2 = 0.05

Kp3 = 0.5
Ki3 = 0
Kd3 = 0.05

Zz1 = (12/20) * (24/28)
Zz2 = 20/36
Zz3 = 24/40
Zz2 = 1
Zz3 = 1


l1 = 0.23
l2 = 0.16
l3 = 0.18

L = 0.2

x = [0.2,0.2, 0.2, 0.2, 0.2, 0.3]
y = [0.2,0.2, 0.2, 0, 0.2, 0]
z = [L,0.2,L,L,L,L]

tata1 = [0, 0, 0, 0, 0, 0]
tata2 = [0, 0, 0, 0, 0, 0]
tata3 = [0, 0, 0, 0, 0, 0]

f = open("result.txt", "w")
for i in range(6):
	theta1_d = atan2(x[i],y[i])
	a1 = atan2((z[i]-l1),((x[i]**2+y[i]**2)**0.5))
	a2 = acos((l2**2 + x[i]**2 + y[i]**2 + (z[i]-l1)**2 - l3**2)/(2*l2*((x[i]**2 + y[i]**2 + (z[i]-l1)**2)**0.5)))
	theta2_d = pi/2 - a1 - a2
	theta3_d = acos((x[i]**2 + y[i]**2 + (z[i]-l1)**2 - l3**2 - l2**2)/(2*l2*l3))
	theta1_d = theta1_d * 180 / pi
	theta2_d = theta2_d * 180 / pi
	theta3_d = theta3_d * 180 / pi
	tata1[i] = theta1_d
	tata2[i] = theta2_d
	tata3[i] = theta3_d
	
	
	
	f.write(str(theta1_d) + " " + str(theta2_d) + " " + str(theta3_d) + "\n")


def q3():
	return -1 * mC.position  *Zz3

def q2():
	return -1 * mB.position * Zz2

def q1():
	return mA.position * Zz1

k = 0


i = 0


while (k==0):
	theta1 = q1()
	theta2 = q2()
	theta3 = q3()
	if (abs(theta1 - tata1[i]) < 10) and (abs(theta2 - tata2[i]) < 10) and (abs(theta3 - tata3[i]) < 10):
		i = i + 1
		f.write("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF" + "\n")
	if i == 6:
		mA.run_direct(duty_cycle_sp = 0)
		mB.run_direct(duty_cycle_sp = 0)
		mC.run_direct(duty_cycle_sp = 0)
		k=1
		break



	theta1 = q1()
	cur_speed1 = mA.speed*Zz1
	sum_e1 += tata1[i]-theta1
	u1 = Kp1*(tata1[i]-theta1) + Ki1*sum_e1 + Kd1*(-cur_speed1)
	if abs(theta1 - tata1[i]) < 3:
		u1 = 0


	theta2 = q2()
	cur_speed2 = mB.speed*Zz2
	sum_e2 += tata2[i]-theta2
	u2 = Kp2*(tata2[i]-theta2) + Ki2*sum_e2 + Kd2*(-cur_speed2)
	u2 = -u2

	theta3 = q3()
	cur_speed3 = mC.speed*Zz3
	sum_e3 += tata3[i]-theta3
	u3 = Kp3*(tata3[i]-theta3) + Ki3*sum_e3 + Kd3*(-cur_speed3)
	u3 = -u3

	b1 = theta1 * pi / 180
	b2 = theta2 * pi / 180
	b3 = theta3 * pi / 180
	p = (l2**2 + l3**2 + 2*cos(b3)*l2*l3)**0.5
	alpha = pi/2 - asin(l3*sin(b3)/p) - b2

	x_out = cos(b1) * p * cos(alpha)
	y_out = sin(b1) * p * cos(alpha)
	z_out = sin(alpha) * p + l1

	f.write(str(x_out) + " " +  str(y_out) + " " + str(z_out) + "\n")

	if abs(u1) > 100:
		u1 = copysign(100, u1)
	if abs(u2) > 100:
		u2 = copysign(100, u2)
	if abs(u3) > 100:
		u3 = copysign(100, u3)



	if ts1.is_pressed or ts2.is_pressed:
		if ts1.is_pressed:
			mA.run_direct(duty_cycle_sp = 50)
			mB.run_direct(duty_cycle_sp = 0)
			mC.run_direct(duty_cycle_sp = 0)
		if ts2.is_pressed:
			mA.run_direct(duty_cycle_sp = -50)
			mB.run_direct(duty_cycle_sp = 0)
			mC.run_direct(duty_cycle_sp = 0)
		if ts1.is_pressed and ts2.is_pressed:
			mA.run_direct(duty_cycle_sp = 0)
			mB.run_direct(duty_cycle_sp = 0)
			mC.run_direct(duty_cycle_sp = 0)
			break
	else:
		mA.run_direct(duty_cycle_sp = u1)
		mB.run_direct(duty_cycle_sp = u2)
		mC.run_direct(duty_cycle_sp = u3)
