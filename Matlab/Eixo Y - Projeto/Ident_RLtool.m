clc
clear all
close all

%% Importando Dados
u =	[	0	0	0	0	0	0	10	10	10	10	10	10	10	10  10	10	10	10	10	10	10	10	10	]'; % degrau  
y1 = [	0	0	0	0	0	0	0	0	6	51	74	78	79	80	80	80	81	81	81	81	81	82	82	]'; % média baixa 0.3M
y2 = [	0	0	0	0	0	0	0	0	11	85	118	121	122	122	122	123	123	123	123	123	123	123	124 ]'; % média alta 1.2M
y3 = [  0	0	0	0	0	0	0	0	10	68	94	95	96	96	97	97	97	97	97	97	97	97	97  ]'; % média 0.6M
y4 = [  0	0	0	0	0	0	0	0	0	113	124	124	124	127	128	128	128	128	128	128	128	128	128 ]'; % máxima 0.6M
y5 = [  0	0	0	0	0	0	0	0	0	38	74	74	75	76	75	77	76	76	78	78	78	78	78 ]';  % mínima 0.6M


%% Parâmetros
N = length(u); % quantidade de amostras
T= 0.04; % período de amostragem
t = 0:T:(N-1)*T; % tempo para simulação

%% Funções de Transferência
Y1 = tf( [-0.0001849 0.601 4.177], [1 -0.5356 0.1912 -0.06649], T );
Y2 = tf( [0.0003743 1.097 6.9], [1 -0.4647 0.1618 -0.04697], T );
Y3 = tf( [0.001112 0.9936 5.355], [1 -0.469 0.182 -0.05863], T );
Y4 = tf( [-0.0002423 0.002128 11.28], [1 -0.1 0.01552 -0.03223], T );
Y5 = tf( [3.58e-05 0.0002902 3.8 3.669], [1 0.02132 -0.0228 -0.001471 -0.02928], T );


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

%Cz = tf( [ 0.0379 -0.01843 ] , [ 1 -1 ] , T );
Cz = tf( [ 0.06183 -0.07155 0.02935 ] , [ 1 -1.061 0.06056 ] , T );

%sim('Control_Validacao');
