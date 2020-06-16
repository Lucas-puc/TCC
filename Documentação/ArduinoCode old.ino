//Inclusão da biblioteca para servo motores
#include <Servo.h>

//Cria os dois servo motores
Servo eixo_x;
Servo eixo_y;

// Cria as variáveis referente as posições dos dois servo motores
int angulo_x = 90;
int angulo_y = 90;

void setup() {
  //Coloca o servo do eixo X no pino 9 e do eixo Y no pino 10
  eixo_x.attach(9);
  eixo_y.attach(10);
  eixo_x.write(angulo_x);
  eixo_y.write(angulo_y);

  //Inicializa a comunicação serial
  Serial.begin(9600);
}

void loop() {
  //Verificando se existem dados na porta serial
  while(Serial.available()>0)
  {  
    //Testa o começo da mensagem
    if(Serial.read() == 'X')
    {
      angulo_x = Serial.parseInt();
      eixo_x.write(angulo_x);
     
      while(Serial.available()>0)
      {
        if(Serial.read() == 'Y')
        {
          angulo_y = Serial.parseInt();
          eixo_y.write(angulo_y);

          while(Serial.available()>0)
          {
            Serial.read();
          }
        }
      }
    }
  } 
}
