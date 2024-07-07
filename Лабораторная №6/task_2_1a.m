experiment = readmatrix("C:\Users\osini\OneDrive\Рабочий стол\Study22-23\ТАУ\Лабораторная №6\все файлы\task2.1a\task2.1_0.5.txt");
        time = data(:,1);
        angle = data(:,2)*pi/180; % перевод из градусов в радианы
plot(time, angle)
