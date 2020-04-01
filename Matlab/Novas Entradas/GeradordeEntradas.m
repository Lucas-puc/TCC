clear all
clc
%Degrau 51 amostras começando no 11
Degrau_Positivo = zeros(51,1);
Degrau_Positivo(11:end,1) = 10;
Degrau_Negativo = Degrau_Positivo*(-1);

%Ruido Branco