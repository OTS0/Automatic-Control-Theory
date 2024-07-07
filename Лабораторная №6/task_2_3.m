syms s t;
g = 3*sin(t+1)+2*cos(t)%задающее воздействие
k= 2.4716
T= 0.0644
Wo=k/(T*s^2 + s) %передаточная функция
[N, D]=numden(Wo)
[Ng,Dg]=numden(laplace(g))% находим образ Лапласа от входа и разделяем на чилитель и знаменатель

syms c c0
Dper=c*Dg*(s+c0)

syms c1 c2 c3 c4 
Nper=c1*s^3+c2*s^2+c3*s+c4
pol=coeffs(Nper*N+Dper*D,s,"All")
needed_pol=coeffs((s+1)*(s+1)*(s+1)*(s+1)*(s+1),s,"All")
sol=solve(pol==needed_pol)

Nper_sol=sym2poly(subs(Nper,[c c0 c1 c2 c3 c4], [sol.c sol.c0 sol.c1 sol.c2 sol.c3 sol.c4]))
%sym2poly() - возвращает коэффициенты полинома
%subs() - заменяет коэффициенты
Dper_sol=sym2poly(subs(Dper,[c c0],[sol.c sol.c0]))