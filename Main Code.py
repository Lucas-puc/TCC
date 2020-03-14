#Bibliotecas e funções utilitárias
import cv2 as cv
import numpy as np
import time
import imutils
import serial
def nada(x):
	pass


#Parâmetros
def_camera = 0          #Define a câmera a ser utilizada (integrada = 0)
def_com = 6             #Define a porta serial utilizada pelo Arduino
def_amostragem = 0.035   #Define a taxa de amostragem em segundos
angulo_X = 90           #Posição inicial do motor responsável pelo eixo X
angulo_Y = 90           #Posição inicial do motor responsável pelo eixo Y



#Objeto para processamento de imagem
class Imagem:
	def __init__(self, camera_num):
		self.camera = cv.VideoCapture(camera_num)
		print("Inicializando Camera...")
		time.sleep(2)


	def __del__(self):
		self.camera.release()
		cv.destroyAllWindows()

	#Função para ajuste de máscara
	def AjusteMascara(self):		
		#Testa se a tela de ajuste de máscara está aberta
		if cv.getWindowProperty('Ajuste de Mascara',1) == -1 :

			#Criação da janela de ajuste de máscara 
			cv.namedWindow("Ajuste de Mascara")
			cv.createTrackbar("Min-H", "Ajuste de Mascara", 0, 179, nada)
			cv.createTrackbar("Min-S", "Ajuste de Mascara", 0, 255, nada)
			cv.createTrackbar("Min-V", "Ajuste de Mascara", 0, 255, nada)
			cv.createTrackbar("Max-H", "Ajuste de Mascara", 0, 179, nada)
			cv.createTrackbar("Max-S", "Ajuste de Mascara", 0, 255, nada)
			cv.createTrackbar("Max-V", "Ajuste de Mascara", 0, 255, nada)

			#Valores Iniciais (pre-config 1):
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 29)
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 86)
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 6)
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)

		#Captura o frame atual
		_, frame = self.camera.read()

		#Suavização da imagem para filtrar ruidos
		frame_suave = cv.GaussianBlur(frame, (11, 11), 0)
		
		#Converte para o color-space de BGR (RGB) para HSV (Hue-Saturation-Value)
		hsv = cv.cvtColor(frame_suave, cv.COLOR_BGR2HSV)

		#Criação da máscara de cor filtrando por parâmetros de HSV mínimos e máximos
		min_h = cv.getTrackbarPos("Min-H", "Ajuste de Mascara")
		min_s = cv.getTrackbarPos("Min-S", "Ajuste de Mascara")
		min_v = cv.getTrackbarPos("Min-V", "Ajuste de Mascara")
		max_h = cv.getTrackbarPos("Max-H", "Ajuste de Mascara")
		max_s = cv.getTrackbarPos("Max-S", "Ajuste de Mascara")
		max_v = cv.getTrackbarPos("Max-V", "Ajuste de Mascara")

		self.cor_min = np.array([min_h, min_s, min_v])
		self.cor_max = np.array([max_h, max_s, max_v])
		mascara = cv.inRange(hsv, self.cor_min, self.cor_max)

		#Realização de Operações Morfológicas para filtrar a máscara e remover pontos indesejados
		mascara = cv.erode(mascara, None, iterations=2)
		mascara = cv.dilate(mascara, None, iterations=2)

		#Encontra os contornos da máscara, os reúne e inicializa a variável correspondente ao centro do círculo
		contornos = cv.findContours(mascara.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		contornos = imutils.grab_contours(contornos)

		#Testa se algum contorno foi encontrado
		if len(contornos) > 0:
			#Usa o maior contorno encontrado para calcular o raio e o centro do circulo
			c = max(contornos, key=cv.contourArea)
			((x, y), raio) = cv.minEnclosingCircle(c)
			#Testa o raio do circulo para evitar ruídos
			if raio > 10:
			    #Desenha o circulo (cor em BGR)
			    cv.circle(frame, (int(x), int(y)), int(raio), (0, 0, 255), 2)
		
		#Mostra a imagem capturada da câmera e da máscara de cor
		cv.imshow("Camera", frame)
		cv.imshow("Mascara", mascara)

	#Função de rastreamento
	def Rastreamento(self):
		#Captura o frame atual
		_, frame = self.camera.read()
		altura, largura,_ = frame.shape

		#Suavização da imagem para filtrar ruidos
		frame_suave = cv.GaussianBlur(frame, (11, 11), 0)
		
		#Converte para o color-space de BGR (RGB) para HSV (Hue-Saturation-Value)
		hsv = cv.cvtColor(frame_suave, cv.COLOR_BGR2HSV)

		#Realização de Operações Morfológicas para filtrar a máscara e remover pontos indesejados
		mascara = cv.inRange(hsv, self.cor_min, self.cor_max)
		mascara = cv.erode(mascara, None, iterations=2)
		mascara = cv.dilate(mascara, None, iterations=2)

		#Encontra os contornos da máscara, os reúne e inicializa a variável correspondente ao centro do círculo
		contornos = cv.findContours(mascara.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		contornos = imutils.grab_contours(contornos)

		#Testa se algum contorno foi encontrado
		if len(contornos) > 0:
			#Usa o maior contorno encontrado para calcular o raio e o centro do circulo
			c = max(contornos, key=cv.contourArea)
			((x, y), raio) = cv.minEnclosingCircle(c)
			#Testa o raio do circulo para evitar ruídos
			if raio > 10:
				#Desenha cruz no centro do circulo
				cv.line(frame, (int(x-raio/4), int(y)), (int(x+raio/4), int(y)), (0, 0, 255), 1)
				cv.line(frame, (int(x), int(y-raio/4)), (int(x), int(y+raio/4)), (0, 0, 255), 1)

		#Desenha uma cruz no centro do frame
		cv.line(frame, (largura//2-10, altura//2), (largura//2+10, altura//2), (255, 0, 0), 1)
		cv.line(frame, (largura//2, altura//2-10), (largura//2, altura//2+10), (255, 0, 0), 1)

		#Mostra a imagem capturada da câmera
		cv.imshow("Camera", frame)

		#Retorna os valores do ponto X, Y, altura e largura
		return x, y, largura, altura




#Função que movimenta os motores de acordo com as variáveis globais
def MoverMotores():
    global angulo_X
    global angulo_Y

    #Saturação
    if angulo_X > 180 : angulo_X = 180 
    if angulo_X < 0 : angulo_X = 0 
    if angulo_Y > 180 : angulo_Y = 180 
    if angulo_Y < 0 : angulo_Y = 0 

    #Envia comando para o arduino
    mensagem = "X" + str(int(angulo_X)) + "Y" + str(int(angulo_Y))
    #print(mensagem)
    mensagem = str.encode(mensagem)
    #arduino.write(mensagem)



#Função de aplicação do Controlador
def Controle():
	global angulo_X
	global angulo_Y
	posX, posY, tamX, tamY = Cam.Rastreamento()
	#Calculo do erro
	erro_X = posX - tamX/2
	erro_Y = tamY/2 - posY

	#Aplica o controle
	controle_X = erro_X/100
	controle_Y = erro_Y/100

	#Ajusta a saída
	angulo_X = angulo_X - controle_X
	angulo_Y = angulo_Y - controle_Y

	#Movimentação dos Motores
	MoverMotores()



#Função de aplicação do degrau e coleta de dados
def Degrau(sentido):
	global angulo_X
	global angulo_Y
	cv.destroyAllWindows()
	if sentido == "cima":
		novo_Y = angulo_Y - 10
		novo_X = angulo_X
	if sentido == "baixo":
		novo_Y = angulo_Y + 10
		novo_X = angulo_X
	if sentido == "esquerda":
		novo_X = angulo_X + 10
		novo_Y = angulo_Y
	if sentido == "direita":
		novo_X = angulo_X + 10
		novo_Y = angulo_Y
	print("N:Angulo X:Posicao X:Angulo Y:Posicao Y")
	N = 0
	while True:
		inicio = time.time()
		if N == 60:
			angulo_X = novo_X
			angulo_Y = novo_Y
			MoverMotores()
		posX, posY, _, _ = Cam.Rastreamento()
		print("%s:%s:%s:%s:%s" % (N,angulo_X,posX,angulo_Y,posY))
		tecla = cv.waitKey(1) #Utilizado por limitação do compilador
		if N == 120:
			break
		N = N+1
		while ((time.time() - inicio) < def_amostragem):
			pass



#                       MAIN CODE		



Cam = Imagem(def_camera) #inicializa camera
modo = 0 #Inicializa com o modo de ajuste da máscara

#Inicialização do Arduino
#arduino = serial.Serial('COM'+str(def_com), 9600, timeout = 1)
time.sleep(2)
print("Inicializando comunicação...")

while True:
        #Modo de ajuste de máscara
	while modo == 0:
		Cam.AjusteMascara()
		tecla = cv.waitKey(1)
		if tecla != -1:
			break
	#Modo com controle aplicado
	while modo == 1:
		inicio = time.time()
		Controle()
		tecla = cv.waitKey(1)		
		if tecla != -1:
			break
		while(time.time()-inicio < def_amostragem):
			pass

	#Leitura de Teclas
	if tecla == 27: #Tecla ESC
		del Cam
		break
        #Seleção de Modos
	if tecla == ord('q'):
		cv.destroyAllWindows()
		modo = 0
	if tecla == ord('w'):
		cv.destroyAllWindows()
		modo = 1
	#Modo captura (Degrau)
	if tecla == ord('8'):
		Degrau("cima")
		cv.destroyAllWindows()
	if tecla == ord('2'):
		Degrau("baixo")
		cv.destroyAllWindows()
	if tecla == ord('6'):
		Degrau("direita")
		cv.destroyAllWindows()
	if tecla == ord('4'):
		Degrau("esquerda")
		cv.destroyAllWindows()
