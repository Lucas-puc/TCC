clc
clear all
close all

% SISTEMA DE ORDEM 3

%% Configurações

ordem = 1;
T = 0.04;


%% Aquisição dos Dados

N = 501;

formatSpec = '%f';

arq = fopen('Degrau.txt','r');
u = fscanf(arq, formatSpec);
u = u;
fclose(arq);

arq = fopen('Resposta Degrau x.txt','r');
y = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Resposta Degrau x.txt','r');
y_degrau = fscanf(arq, formatSpec);
fclose(arq);

%% Escreva seu código aqui

tf_digital = MinimosQuadrados(N, y, u, T, ordem);

tf_analogico = d2c(tf_digital);



%% Validação do Modelo

sim('TesteDegrauMinQuadSimulink')