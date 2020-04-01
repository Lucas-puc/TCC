clc
clear all
close all

% SISTEMA DE ORDEM 3

%% Configurações

ordem = 1;
T = 0.04;


%% Aquisição dos Dados

formatSpec = '%f';

arq = fopen('Entrada/Entrada_RuidoBranco.txt','r');
Ruido_Branco = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Entrada/Entrada_Degrau_Positivo.txt','r');
degrau_positivo = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Entrada/Entrada_Degrau_Negativo.txt','r');
degrau_negativo = fscanf(arq, formatSpec);
fclose(arq);

%%
arq = fopen('Saida/Resposta ao Ruido Branco no eixo X.txt','r');
resposta_rb_X = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Saida/Resposta ao Ruido Branco no eixo Y.txt','r');
resposta_rb_Y = fscanf(arq, formatSpec);
fclose(arq);
%%
arq = fopen('Saida/Resposta ao Degrau Positivo no eixo X.txt','r');
resposta_deg_pos_X = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Saida/Resposta ao Degrau Negativo no eixo X.txt','r');
resposta_deg_neg_X = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Saida/Resposta ao Degrau Positivo no eixo Y.txt','r');
resposta_deg_pos_Y = fscanf(arq, formatSpec);
fclose(arq);

arq = fopen('Saida/Resposta ao Degrau Negativo no eixo Y.txt','r');
resposta_deg_neg_Y = fscanf(arq, formatSpec);
fclose(arq);


%% Escreva seu código aqui

u = degrau_negativo;
y = resposta_deg_neg_X;
N = length(u);
tf_digital_dnX = MinimosQuadrados(N, y, u, T, ordem);

u = degrau_positivo;
y = resposta_deg_pos_X;
N = length(u);
tf_digital_dpX = MinimosQuadrados(N, y, u, T, ordem);

u = Ruido_Branco;
y = resposta_rb_X;
N = length(u);
tf_digital_wnX = MinimosQuadrados(N, y, u, T, ordem);

%% Validação do Modelo
degXp.time = 1:51;
degXp.signals.values = resposta_deg_pos_X;
degXp.signals.dimensions =1;

degXn.time = 1:51;
degXn.signals.values = resposta_deg_neg_X;
degXn.signals.dimensions =1;

sim('TesteDegrauMinQuadSimulinkX')


%% Escreva seu código aqui

u = degrau_negativo;
y = resposta_deg_neg_Y;
N = length(u);
tf_digital_dnY = MinimosQuadrados(N, y, u, T, ordem);

u = degrau_positivo;
y = resposta_deg_pos_Y;
N = length(u);
tf_digital_dpY = MinimosQuadrados(N, y, u, T, ordem);

u = Ruido_Branco;
y = resposta_rb_Y;
N = length(u);
tf_digital_wnY = MinimosQuadrados(N, y, u, T, ordem);

%% Validação do Modelo
degYp.time = 1:51;
degYp.signals.values = resposta_deg_pos_Y;
degYp.signals.dimensions =1;
degYn.time = 1:51;
degYn.signals.values = resposta_deg_neg_Y;
degYn.signals.dimensions =1;

sim('TesteDegrauMinQuadSimulinkY')