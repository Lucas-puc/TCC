clc
clear all
close all

%% Importando Dados
u =	[	0	0	0	0	0	0	10	10	10	10	10	10	10	10  10	10	10	10	10	10	10	10	10	]'; % degrau  
y1 = [	0	0	0	0	0	0	0	0	16	81	98	102	102	102	102	102	102	102	102	102	102	102	102 ]'; % média baixa 0.3M
y2 = [	0	0	0	0	0	0	0	0	22	87	110	112	113	114	114	114	114	114	114	114	114	114	114 ]'; % média alta 1.2M
y3 = [	0	0	0	0	0	0	0	0	23	89	105	109	109	109	109	109	109	109	109	109	109	109	109 ]'; % média 0.6M

%% Parâmetros
N = length(u); % quantidade de amostras
T= 0.04; % período de amostragem
t = 0:T:(N-1)*T; % tempo para simulação

%% Funções de Transferência
Y1 = tf( [3.48e-6 1.6 6.079], [1 -0.2635 0.007111 0.009379], T );
Y2 = tf( [0.0003065 2.198 5.651], [1 -0.3892 0.1132 -0.03574], T );
Y3 = tf( [-1.216e-06 2.3 6.046], [1 -0.2409 -0.004502 0.01131], T );

%% Para simulação e validação
y1_data.time = t;
y1_data.signals.values = y1;
y1_data.signals.dimensions =1;

y2_data.time = t;
y2_data.signals.values = y2;
y2_data.signals.dimensions =1;

y3_data.time = t;
y3_data.signals.values = y3;
y3_data.signals.dimensions =1;
sim('Ident_Validacao');

%% Projeto de Controle
Gz = stack(1,Y3,Y2,Y1);

%Cz = tf( [0.036639 -0.0293112 0.0081521775], [1 -1.14 0.14], T );
Cz = tf( [ 0.04809 -0.03559 0.008265 ] , [ 1 -1.117 0.1168 ], T );
sim('Control_Validacao');
