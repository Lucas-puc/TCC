import time
import serial

class Comando:
    def __init__(self, com, baud_rate):
        self.p_serial = serial.Serial('COM' + str(com), baud_rate)
        time.sleep(2)
        self.angulo_x = 90
        self.angulo_y = 90
        self.mover(self.angulo_x, self.angulo_y)

    def mover(self, angulo_x, angulo_y):

        if angulo_x > 180:
            angulo_x = 180
        if angulo_x < 0:
            angulo_x = 0
        if angulo_y > 180:
            angulo_y = 180
        if angulo_y < 0:
            angulo_y = 0

        self.angulo_x = angulo_x
        self.angulo_y = angulo_y
        palavra = "X" + str(int(1000+self.angulo_x*1000/180)) + "Y" + str(int(1000+self.angulo_y*1000/180)) + "f"
        palavra = str.encode(palavra)
        self.p_serial.write(palavra)

    def atual(self):
        return [self.angulo_x, self.angulo_y]

    def wasd(self, tecla):
        if tecla == ord('w'):
            angulo_y = self.angulo_y + 10
            angulo_x = self.angulo_x
        if tecla == ord('a'):
            angulo_y = self.angulo_y
            angulo_x = self.angulo_x + 10
        if tecla == ord('s'):
            angulo_y = self.angulo_y - 10
            angulo_x = self.angulo_x
        if tecla == ord('d'):
            angulo_y = self.angulo_y
            angulo_x = self.angulo_x - 10

        if angulo_x > 180:
            angulo_x = 180
            print("Fora de Alcance! Angulo X+")
        if angulo_x < 0:
            angulo_x = 0
            print("Fora de Alcance! Angulo X-")
        if angulo_y > 180:
            angulo_y = 180
            print("Fora de Alcance! Angulo Y+")
        if angulo_y < 0:
            angulo_y = 0
            print("Fora de Alcance! Angulo Y-")

        self.mover(angulo_x, angulo_y)
