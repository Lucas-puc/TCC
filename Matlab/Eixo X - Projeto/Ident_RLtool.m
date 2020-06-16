clc
clear all
close all

%% Importando Dados
u =	[	0	0	0	0	0	0	10	10	10	10	10	10	10	10  10	10	10	10	10	10	10	10	10	]'; % degrau  
y1 = [	0	0	0	0	0	0	0	0	16	81	98	102	102	102	102	102	102	102	102	102	102	102	102 ]'; % média baixa 0.3M
y2 = [	0	0	0	0	0	0	0	0	22	87	110	112	113	114	114	114	114	114	114	114	114	114	114 ]'; % média alta 1.2M
y3 = [	0	0	0	0	0	0	0	0	23	89	105	109	109	109	109	109	109	109	109	109	109	109	109 ]'; % média 0.6M
y4 = [  0	0	0	0	0	0	0	0	19	87	112	114	119	119	119	119	119	120	120	119	119	119	120 ]'; %máxima 0.6M
y5 = [  0	0	0	0	0	0	0	0	5	71	97	94	106	99	99	99	99	99	99	99	99	99	99 ]'; %minima 0.6M


%% Parâmetros
N = length(u); % quantidade de amostras
T= 0.04; % período de amostragem
t = 0:T:(N-1)*T; % tempo para simulação

%% Funções de Transferência
Y1 = tf( [3.48e-6 1.6 6.079], [1 -0.2635 0.007111 0.009379], T );
Y2 = tf( [0.0003065 2.198 5.651], [1 -0.3892 0.1132 -0.03574], T );
Y3 = tf( [-1.216e-06 2.3 6.046], [1 -0.2409 -0.004502 0.01131], T );
Y4 = tf( [0.001266 1.892 6.116], [1 -0.3787 0.0893 -0.04015 ], T );
Y5 = tf( [0.003993 0.4917 6.77 4.861], [1 0.3475 -0.08834 -0.1231 0.08894], T );

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

y4_data.time = t;
y4_data.signals.values = y4;
y4_data.signals.dimensions =1;

y5_data.time = t;
y5_data.signals.values = y5;
y5_data.signals.dimensions =1;


%sim('Ident_Validacao');

%% Projeto de Controle
Gz = stack(1,Y5,Y4,Y3,Y2,Y1);


%Cz = tf( [ 0.03852 -0.01682 ] , [ 1 -1] , T );
Cz = tf( [ 0.06455 -0.03577 0.005091 ] , [ 1 -0.6037 -0.3963 ] , T );

%sim('Control_Validacao');
