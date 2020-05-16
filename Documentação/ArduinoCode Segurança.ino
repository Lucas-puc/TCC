//Inclusão da biblioteca para servo motores
#include <Servo.h>

//Cria os dois servo motores
Servo eixo_x;
Servo eixo_y;

// Cria as variáveis referente as posições dos dois servo motores
int angulo_x = 45;
int angulo_y = 45;
int angulo_x_anterior = 0;
int angulo_y_anterior = 0;



void setup() {
  //Coloca o servo do eixo X no pino 9 e do eixo Y no pino 10
  eixo_x.attach(9);
  eixo_y.attach(10);

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
      if(angulo_x !=  angulo_x_anterior)
      {
        eixo_x.write(angulo_x);
      }
      
      while(Serial.available()>0)
      {
        if(Serial.read() == 'Y')
        {
          angulo_y = Serial.parseInt();
          if(angulo_y !=  angulo_y_anterior)
          {
            eixo_y.write(angulo_y);
          }
          while(Serial.available()>0)
          {
            Serial.read();
          }
        }
      }
    }
    angulo_x_anterior = angulo_x;
    angulo_y_anterior = angulo_y;
  } 
}
