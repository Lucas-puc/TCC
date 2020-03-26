clc
clear all
close all

% SISTEMA DE ORDEM 2

%% Configurações

ordem = 8;
T = 0.03;
ttotal = 5;
seed1=23341;
power1= 10;
stepsize=1;

%% Aquisição dos Dados

N = 30;
u =    [0
        0
        0
        0
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
        10
        10
        10
        10];
y =    [0.011062622
        0.104248047
        0.101226807
        -0.128890991
        -0.015838623
        0.024887085
        -0.015838623
        0.104248047
        0.122879028
        -0.024383545
        0.108764648
        0.000289917
        4.109161377
        60.8742218
        113.3762665
        112.1957245
        110.7453613
        123.6091614
        123.556572
        122.4499664
        123.1571274
        122.5686188
        123.0377731
        123.121727
        123.1058426
        122.9849548
        123.1091614
        123.121727
        123.0642776
        123.121727];

%% Escreva seu código aqui

tf_digital = MinimosQuadrados(N, y, u, T, ordem);

tf_analogico = d2c(tf_digital);


%% Validação do Modelo

sim('TesteDegrauMinQuadSimulink')