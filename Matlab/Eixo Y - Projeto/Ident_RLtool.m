clc
clear all
close all

%% Importando Dados
u =	[	0	0	0	0	0	0	10	10	10	10	10	10	10	10  10	10	10	10	10	10	10	10	10	]'; % degrau  
y1 = [	0	0	0	0	0	0	0	0	6	51	74	78	79	80	80	80	81	81	81	81	81	82	82	]'; % média baixa 0.3M
y2 = [	0	0	0	0	0	0	0	0	11	85	118	121	122	122	122	123	123	123	123	123	123	123	124 ]'; % média alta 1.2M
y3 = [  0	0	0	0	0	0	0	0	10	68	94	95	96	96	97	97	97	97	97	97	97	97	97  ]'; % média 0.6M

%% Parâmetros
N = length(u); % quantidade de amostras
T= 0.04; % período de amostragem
t = 0:T:(N-1)*T; % tempo para simulação

%% Funções de Transferência
Y1 = tf( [-0.0001849 0.601 4.177], [1 -0.5356 0.1912 -0.06649], T );
Y2 = tf( [0.0003743 1.097 6.9], [1 -0.4647 0.1618 -0.04697], T );
Y3 = tf( [0.001112 0.9936 5.355], [1 -0.469 0.182 -0.05863], T );

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

%Cz = tf( [0.07466 -0.07332 0.02345 ], [ 1 -1.206 0.2058 ], T );
Cz = tf( [ 0.05322 -0.04188 0.01001 ], [1 -1.108 0.1082], T);

sim('Control_Validacao');
