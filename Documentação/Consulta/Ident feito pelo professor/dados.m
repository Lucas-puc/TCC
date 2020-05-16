clc
clear all
close all

u = [ 
0
0
0
0
0
0
10
10
10
10
10
10
10
10
10
10
10
10
10
10
10
10
10 ];

y1 = [  
0
0
0
0
0
0
0
1
7
76
104
109
109
109
109
109
109
109
109
109
109
109
109  ];

y2 = [  
0
0
0
0
0
0
0
0
13
82
107
110
111
111
111
111
111
111
111
111
111
111
111 ];

y3 = [  
0
0
0
0
0
0
0
0
15
85
110
113
114
115
114
114
114
114
114
114
114
114
114 ];

N = length(u);
T= 1; % sampling period
t = 0:T:(N-1);

figure
stairs(t,u)
hold on
stairs(t,y1)
hold on
stairs(t,y2)
hold on
stairs(t,y3)

Gs1 = tf( [0         0   62.9637] , [1.0000    4.7553    5.7745] , 'iodelay' , 2  );
Gs2 = tf( [0         0   82.8235] , [1.0000    5.6921    7.4630] , 'iodelay' , 2  );
Gs3 = tf( [0         0   90.2451] , [1.0000    5.9630    7.9116] , 'iodelay' , 2  );

% Transfer Function Model - Discrete - 3 poles - 3 zeros

Gz1 = tf( [ 0    0.1000    0.5587    6.6604] , [1.0000   -0.4146    0.0980   -0.0120] , T );
Gz2 = tf( [ 0    0.0001    1.2989    6.4170] , [1.0000   -0.3761    0.0885   -0.0176] , T );
Gz3 = tf( [ 0    0.0002    1.4982    6.4535] , [1.0000   -0.3704    0.0823   -0.0150] , T );

Gz = stack(1,Gz2,Gz1,Gz3);

k0 = 8;
y1c = y1(k0:end)/u(end);
y2c = y2(k0:end)/u(end);
y3c = y3(k0:end)/u(end);

figure
step(Gz1);
hold on
stairs(y1c,'-.');
hold on
step(Gz2);
hold on
stairs(y2c,'-.');
hold on
step(Gz3);
hold on
stairs(y3c,'-.');

% RLTOOL Design for Gz

% rltool(Gz)

Cz = tf( [0.0398   -0.0239    0.0041] , [1    -1     0] , T );

% u(k) = u(k-1) + 0.0398*e(k) - 0.0239*e(k-1) + 0.0041*e(k-2)
