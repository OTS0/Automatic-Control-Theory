A = [5 -7 -5 1;
    -7 5 -1 5;
    -5 -1 5 7;
    1 5 7 5]
B = [14;10;6;2]
C = [1 -1 3 3;
2 2 -2 2]
%Находим собственные числа и опредяляем их управляемость и наблюдаемость
S = eig(A)
S = eig(A,'matrix')
l = [S(1,1) S(2,2) S(3,3) S(4,4)]

for v=l
    v
    r = rank([A-v*eye(4) B])
    r_nabl = rank([A-v*eye(4); C])
end
%Далее вычислим 
G  = [-8 0 0 0;
0 -3 0 0;
0 0 -2 0;
0 0 0 -1]
Y1 = [0 1 1 1]
Y = [0 0;1 1;1 1;1 1]

cvx_begin sdp
variable Q(4, 4)
variable P(4, 4)
A*P - P*G == B*Y1
G*Q - Q*A == Y*C
cvx_end

det(Q)
det(P)
L = inv(Q)*Y
K = -Y1*inv(P)
eig(A+L*C)%checking 
eig(A+B*K)%checking 