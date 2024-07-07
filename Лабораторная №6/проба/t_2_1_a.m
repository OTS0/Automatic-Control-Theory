data = readmatrix("C:\Users\osini\OneDrive\Рабочий стол\Study22-23\ТАУ\Лабораторная №6\все файлы\task2.2c\task2.2c.txt");
time = data(:,1);
angle = data(:,2); % перевод из градусов в радианы
T = 0.0644
k = 2.4716

hold on
plot(time, angle,'b-')
grid on;
title('График угла поворота двигателя от времени при линейно возрастающим сигнале g(t) = t^3');
xlabel('t, с');
ylabel(' θ, рад ');
plot (out.simout, 'r-')

legend('эксперимент','математическая модель')
