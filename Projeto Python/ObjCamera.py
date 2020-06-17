import cv2 as cv
import numpy as np
import time
import imutils


# noinspection PyUnusedLocal
def nada(x):
    pass

# noinspection PyAttributeOutsideInit
def fechar_janelas():
    cv.destroyAllWindows()


# noinspection PyAttributeOutsideInit
class Imagem:
    def __init__(self, camera_num):
        print("Inicializando Camera...")
        self.camera = cv.VideoCapture(camera_num)
        time.sleep(2)
        self.x = 100
        self.y = 100
        self.raio = 0
        self.inicio_status = 1
        self.tecla = cv.waitKey(1)

    def __del__(self):
        self.camera.release()
        cv.destroyAllWindows()

    # Pré configurações
    def pre_config(self, numero):
        if numero == 1:
            # Valores Iniciais (pre-config 1):
            cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 37)
            cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 79)
            cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 26)
            cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
            cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
            cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
        if numero == 2:
            # Valores Iniciais (pre-config 2):
            cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 0)
            cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 117)
            cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 73)
            cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 4)
            cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
            cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
        if numero == 3:
            # Valores Iniciais (pre-config 3):
            cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 5)
            cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 139)
            cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 113)
            cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 28)
            cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 248)
            cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
        if numero == 4:
            # Valores Iniciais (pre-config 4):
            cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 77)
            cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 77)
            cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 0)
            cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 131)
            cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 222)
            cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 125)
        if numero == 0:
            # Utilizar os valores atuais
            cv.setTrackbarPos("Min-H", "Ajuste de Mascara", self.cor_min[0])
            cv.setTrackbarPos("Min-S", "Ajuste de Mascara", self.cor_min[1])
            cv.setTrackbarPos("Min-V", "Ajuste de Mascara", self.cor_min[2])
            cv.setTrackbarPos("Max-H", "Ajuste de Mascara", self.cor_max[0])
            cv.setTrackbarPos("Max-S", "Ajuste de Mascara", self.cor_max[1])
            cv.setTrackbarPos("Max-V", "Ajuste de Mascara", self.cor_max[2])

    # Função para ajuste de máscara
    def ajuste_mascara(self):
        # Testa se a tela de ajuste de máscara está aberta
        if cv.getWindowProperty('Ajuste de Mascara', 1) == -1:

            # Criação da janela de ajuste de máscara
            cv.namedWindow("Ajuste de Mascara")
            cv.resizeWindow("Ajuste de Mascara", 350, 300)
            cv.createTrackbar("Min-H", "Ajuste de Mascara", 0, 179, nada)
            cv.createTrackbar("Min-S", "Ajuste de Mascara", 0, 255, nada)
            cv.createTrackbar("Min-V", "Ajuste de Mascara", 0, 255, nada)
            cv.createTrackbar("Max-H", "Ajuste de Mascara", 0, 179, nada)
            cv.createTrackbar("Max-S", "Ajuste de Mascara", 0, 255, nada)
            cv.createTrackbar("Max-V", "Ajuste de Mascara", 0, 255, nada)

            # Valores já existentes:
            if self.inicio_status == 0:
                self.pre_config(0)
            else:
                # Primeiro loop do sistema
                self.pre_config(1)
                self.inicio_status = 0

        # Captura o frame atual
        _, frame = self.camera.read()
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

        # Suavização da imagem para filtrar ruidos
        frame_suave = cv.GaussianBlur(frame, (11, 11), 0)

        # Converte para o color-space de BGR (RGB) para HSV (Hue-Saturation-Value)
        hsv = cv.cvtColor(frame_suave, cv.COLOR_BGR2HSV)

        # Criação da máscara de cor filtrando por parâmetros de HSV mínimos e máximos
        min_h = cv.getTrackbarPos("Min-H", "Ajuste de Mascara")
        min_s = cv.getTrackbarPos("Min-S", "Ajuste de Mascara")
        min_v = cv.getTrackbarPos("Min-V", "Ajuste de Mascara")
        max_h = cv.getTrackbarPos("Max-H", "Ajuste de Mascara")
        max_s = cv.getTrackbarPos("Max-S", "Ajuste de Mascara")
        max_v = cv.getTrackbarPos("Max-V", "Ajuste de Mascara")

        self.cor_min = np.array([min_h, min_s, min_v])
        self.cor_max = np.array([max_h, max_s, max_v])
        mascara = cv.inRange(hsv, self.cor_min, self.cor_max)

        # Realização de Operações Morfológicas para filtrar a máscara e remover pontos indesejados
        mascara = cv.erode(mascara, None, iterations=2)
        mascara = cv.dilate(mascara, None, iterations=2)

        # Encontra os contornos da máscara, os reúne e inicializa a variável correspondente ao centro do círculo
        contornos = cv.findContours(mascara.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)

        # Testa se algum contorno foi encontraod
        if len(contornos) > 0:
            # Usa o maior contorno encontrado para calcular o raio e o centro do circulo
            c = max(contornos, key=cv.contourArea)
            ((self.x, self.y), raio) = cv.minEnclosingCircle(c)
            # Testa o raio do circulo para evitar ruídos
            if raio > 10:
                # Desenha o circulo (cor em BGR)
                cv.circle(frame, (int(self.x), int(self.y)), int(raio), (0, 0, 255), 2)

        # Mostra a imagem capturada da câmera e da máscara de cor
        cv.imshow("Camera", frame)
        cv.imshow("Mascara", mascara)
        self.tecla = cv.waitKey(1)

    # Função de rastreamento
    def rastreamento(self):
        # Captura o frame atual
        _, frame = self.camera.read()
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
        altura, largura, _ = frame.shape

        # Suavização da imagem para filtrar ruidos
        frame_suave = cv.GaussianBlur(frame, (11, 11), 0)

        # Converte para o color-space de BGR (RGB) para HSV (Hue-Saturation-Value)
        hsv = cv.cvtColor(frame_suave, cv.COLOR_BGR2HSV)

        # Realização de Operações Morfológicas para filtrar a máscara e remover pontos indesejados
        mascara = cv.inRange(hsv, self.cor_min, self.cor_max)
        mascara = cv.erode(mascara, None, iterations=2)
        mascara = cv.dilate(mascara, None, iterations=2)

        # Encontra os contornos da máscara, os reúne e inicializa a variável correspondente ao centro do círculo
        contornos = cv.findContours(mascara.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contornos = imutils.grab_contours(contornos)
        if len(contornos) == 0:
            self.raio = 0

        # Testa se algum contorno foi encontrado
        if len(contornos) > 0:
            # Usa o maior contorno encontrado para calcular o raio e o centro do circulo
            c = max(contornos, key=cv.contourArea)
            ((self.x, self.y), self.raio) = cv.minEnclosingCircle(c)
            # Testa o raio do circulo para evitar ruídos
            if self.raio > 10:
                # Desenha cruz no centro do circulo
                cv.line(frame, (int(self.x - self.raio / 4), int(self.y)), (int(self.x + self.raio / 4), int(self.y)),
                        (0, 0, 255), 1)
                cv.line(frame, (int(self.x), int(self.y - self.raio / 4)), (int(self.x), int(self.y + self.raio / 4)),
                        (0, 0, 255), 1)

        # Desenha uma cruz no centro do frame
        cv.line(frame, (largura // 2 - 10, altura // 2), (largura // 2 + 10, altura // 2), (255, 0, 0), 1)
        cv.line(frame, (largura // 2, altura // 2 - 10), (largura // 2, altura // 2 + 10), (255, 0, 0), 1)

        # Mostra a imagem capturada da câmera
        cv.imshow("Camera", frame)
        self.tecla = cv.waitKey(1)
        # Retorna os valores de erro até o centro e raio
        return int(self.x - largura / 2), int(self.y - altura / 2), self.raio

    def tecla_pressionada(self):
        return self.tecla
