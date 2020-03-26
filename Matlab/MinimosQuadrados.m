function TF_digital = MinimosQuadrados(N, y, u, T, ordem)

Y = y(1+ordem:N);

I = zeros(N-ordem,ordem*2+1);

for i=1:(N-ordem)
    I(i,:) = [flip(y(i:i+ordem-1)') flip(u(i:i+ordem)')];
end

Theta = (inv(I'*I))*I'*Y;

TF_digital = tf(Theta(ordem+1:end)', [1 -Theta(1:ordem)'], T);


end
