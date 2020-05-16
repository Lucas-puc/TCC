#Bibliotecas e funções utilitárias
import cv2 as cv
import numpy as np
import time
import imutils
import serial
from datetime import datetime
def nada(x):
	pass


#Parâmetros
def_camera = 0          #Define a câmera a ser utilizada (integrada = 0)
def_com = 6            #Define a porta serial utilizada pelo Arduino
def_amostragem = 0.04   #Define a taxa de amostragem em segundos
angulo_X = 90           #Posição inicial do motor responsável pelo eixo X
angulo_Y = 90           #Posição inicial do motor responsável pelo eixo Y



#Objeto para processamento de imagem
class Imagem:
	def __init__(self, camera_num):
		self.camera = cv.VideoCapture(camera_num)
		print("Inicializando Camera...")
		time.sleep(2)
		self.x = 100
		self.y = 100
		self.raio = 0
		self.inicio_status = 1

	def __del__(self):
		self.camera.release()
		cv.destroyAllWindows()

	#Pré configurações
	def PreConfig(self, numero):
		if numero == 1:
			#Valores Iniciais (pre-config 1):
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 37)
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 79)
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 26)
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
		if numero == 2:
			#Valores Iniciais (pre-config 2):
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 15)
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 98)
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 18)
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 32)
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 91)
		if numero == 3:
			#Valores Iniciais (pre-config 3):
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 5)
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 139)
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 113)
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 28)
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 248)
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
		if numero == 4:
			#Valores Iniciais (pre-config 4):
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 77)
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 77)
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 0)
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 131)
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 222)
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 125)
		if numero == 0:
			#Utilizar os valores atuais
			cv.setTrackbarPos("Min-H", "Ajuste de Mascara", self.cor_min[0])
			cv.setTrackbarPos("Min-S", "Ajuste de Mascara", self.cor_min[1])
			cv.setTrackbarPos("Min-V", "Ajuste de Mascara", self.cor_min[2])
			cv.setTrackbarPos("Max-H", "Ajuste de Mascara", self.cor_max[0])
			cv.setTrackbarPos("Max-S", "Ajuste de Mascara", self.cor_max[1])
			cv.setTrackbarPos("Max-V", "Ajuste de Mascara", self.cor_max[2])
			


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
			
			#Valores já existentes:
			if self.inicio_status == 0:                        
				self.PreConfig(0)
			else:
				#Primeiro loop do sistema
				self.PreConfig(1)
				self.inicio_status = 0			

		#Captura o frame atual
		_, frame = self.camera.read()
		frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

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

		#Testa se algum contorno foi encontraod
		if len(contornos) > 0:
			#Usa o maior contorno encontrado para calcular o raio e o centro do circulo
			c = max(contornos, key=cv.contourArea)
			((self.x, self.y), raio) = cv.minEnclosingCircle(c)
			#Testa o raio do circulo para evitar ruídos
			if raio > 10:
				#Desenha o circulo (cor em BGR)
				cv.circle(frame, (int(self.x), int(self.y)), int(raio), (0, 0, 255), 2)

		#Imegem com comandos
		comandos = cv.imread("Outros/Comandos.png")
		
		#Mostra a imagem capturada da câmera e da máscara de cor
		cv.imshow("Camera", frame)
		cv.imshow("Mascara", mascara)
		cv.imshow("Comandos", comandos)

	#Função de rastreamento
	def Rastreamento(self):
		#Captura o frame atual
		_, frame = self.camera.read()
		frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
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
			((self.x, self.y), self.raio) = cv.minEnclosingCircle(c)
			#Testa o raio do circulo para evitar ruídos
			if self.raio > 10:
				#Desenha cruz no centro do circulo
				cv.line(frame, (int(self.x-self.raio/4), int(self.y)), (int(self.x+self.raio/4), int(self.y)), (0, 0, 255), 1)
				cv.line(frame, (int(self.x), int(self.y-self.raio/4)), (int(self.x), int(self.y+self.raio/4)), (0, 0, 255), 1)

		#Desenha uma cruz no centro do frame
		cv.line(frame, (largura//2-10, altura//2), (largura//2+10, altura//2), (255, 0, 0), 1)
		cv.line(frame, (largura//2, altura//2-10), (largura//2, altura//2+10), (255, 0, 0), 1)

		#Mostra a imagem capturada da câmera
		cv.imshow("Camera", frame)

		
		#Retorna os valores de erro até o centro e raio
		return int(self.x - largura/2), int(self.y - altura/2), self.raio




#Funções que movimenta os motores de acordo com as variáveis globais
def MoverMotores(valorX, valorY):
	global angulo_X
	global angulo_Y
	if valorX != 0 or valorY != 0:
		angulo_X = angulo_X + valorX
		angulo_Y = angulo_Y + valorY
		if angulo_X > 180 : angulo_X = 180 
		if angulo_X < 0 : angulo_X = 0
		if angulo_Y > 180 : angulo_Y = 180 
		if angulo_Y < 0 : angulo_Y = 0 
		mensagem = "X" + str(int(angulo_X)) + "Y" + str(int(angulo_Y)) + "f"
		mensagem = str.encode(mensagem)
		arduino.write(mensagem)

def AjustaMotores():
	global angulo_X
	global angulo_Y
	mensagem = "X" + str(int(angulo_X)) + "Y" + str(int(angulo_Y)) + "f"
	mensagem = str.encode(mensagem)
	arduino.write(mensagem)


		

def Centraliza():
	print("Centralizando Camera....")
	while True:
		time.sleep(2)
		erroX, erroY, _ = Cam.Rastreamento()
		done = True
		if erroX > 3:
			MoverMotores(-1,0)
			done = False
		if erroX < -3:
			MoverMotores(1,0)
			done = False
		if erroY > 3:
			MoverMotores(0,-1)
			done = False
		if erroY < -3:
			MoverMotores(0,1)
			done = False
		if done: break
		tecla = cv.waitKey(1)
		if tecla != -1:
			break
		time.sleep(1)


#Função para coletar dados automaticamente
def EnsaioIdentX():

	#Centralização da Camera
	cv.destroyAllWindows()
	print("Inicializando processo automatizado de coleta de dados - Eixo X")
	agora = datetime.now()
	inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
	print("Inicio: " + inicio_info)
	Centraliza()

	#Importando sinal de degrau
	entrada_txt = "Entrada/Degrau.txt"
	sinal = open(entrada_txt, "r")
	N = len(sinal.readlines())
	u = [None]*N
	value = [None]*N
	sinal = open(entrada_txt, "r")
	k = 0
	for line in sinal:
		u[k] = float(line.rstrip())
		k = k+1
	sinal.close()
	_, _, raio_inicio = Cam.Rastreamento()

	

	#Processo no eixo X                
	print("Camera centralizada. Iniciando processo de ensaios para o eixo X.")
	
	for m in range(0,100):        
		tudo_certo = False
		
		while not tudo_certo:			
			inicioX, _, _ = Cam.Rastreamento()
			aux = 1
			if m % 2 == 0: aux = -1
			if m < 50: aux = -1
			if m < 25: aux = 1
			tudo_certo = True
			
			for n in range(N):
				inicio = time.perf_counter()
				tecla = cv.waitKey(1) #Utilizado por limitação do compilador
				if n > 0 and u[n] != u[n-1]: MoverMotores(aux*u[n],0)
				value[n], _, _ = Cam.Rastreamento()
				while time.perf_counter() - inicio < def_amostragem:
					pass
				if (time.perf_counter() - inicio) > 0.045 :
					print("Erro! Tempo de amostragem excedido: %s" %(time.perf_counter() - inicio))
					tudo_certo = False
		
			saida_txt = "Saida/X/Saida" + str(m+1) + ".txt"
			resposta = open(saida_txt,"w")
			
			for k in range(N):
				resposta.write(str((value[k] - inicioX)) + "\n")
				
			resposta.close()
			time.sleep(1)
			MoverMotores(-aux*u[N-1], 0)
			time.sleep(1)
			errX, _, _ = Cam.Rastreamento()
			if abs(inicioX - errX) > 5 : Centraliza()
			time.sleep(1)

	print("Processo de coleta finalizado.")
	agora = datetime.now()
	final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
	print("Final: " + final_info)
	raio_txt = "Saida/X/Info Ensaio.txt"
	info_raio = open(raio_txt,"w")
	info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo X\n")
	info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
	info_raio.write("Inicio: " + inicio_info + "\n")
	info_raio.write("Final: " + final_info + "\n")
	info_raio.close()





def EnsaioIdentY():

	#Centralização da Camera
	cv.destroyAllWindows()
	print("Inicializando processo automatizado de coleta de dados")
	agora = datetime.now()
	inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
	print("Inicio: " + inicio_info)
	Centraliza()

	#Importando sinal de degrau
	entrada_txt = "Entrada/Degrau.txt"
	sinal = open(entrada_txt, "r")
	N = len(sinal.readlines())
	u = [None]*N
	value = [None]*N
	
	sinal = open(entrada_txt, "r")
	k = 0
	for line in sinal:
		u[k] = float(line.rstrip())
		k = k+1
	sinal.close()
	_, _, raio_inicio = Cam.Rastreamento()

	

	#Processo no eixo Y               
	print("Camera centralizada. Iniciando processo de ensaios para o eixo Y.")
	
	for m in range(0,100):        
		tudo_certo = False
		while not tudo_certo:
			_, inicioY, _ = Cam.Rastreamento()

			aux = 1
			if m % 2 == 0: aux = -1
			if m < 50: aux = -1
			if m < 25: aux = 1
			
			tudo_certo = True
			for n in range(N):
				inicio = time.perf_counter()
				tecla = cv.waitKey(1) #Utilizado por limitação do compilador
				if n > 0 and u[n] != u[n-1]: MoverMotores(0,aux*u[n])
				_, value[n], _ = Cam.Rastreamento()
				while time.perf_counter() - inicio < def_amostragem:
					pass
				if (time.perf_counter() - inicio) > 0.045 :
					print("Erro! Tempo de amostragem excedido: %s" %(time.perf_counter() - inicio))
					tudo_certo = False

			saida_txt = "Saida/Y/Saida" + str(m+1) + ".txt"
			resposta = open(saida_txt,"w")
			for k in range(N):
				resposta.write(str((value[k] - inicioY)) + "\n")
			resposta.close()
			time.sleep(1)
			MoverMotores(0, -aux*u[N-1])
			time.sleep(1)
			_, errY, _ = Cam.Rastreamento()
			if abs(inicioY - errY) > 5 : Centraliza()
			time.sleep(1)

	print("Processo de coleta finalizado.")
	agora = datetime.now()
	final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
	print("Final: " + final_info)
	raio_txt = "Saida/Y/Info Ensaio.txt"
	info_raio = open(raio_txt,"w")
	info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo Y\n")
	info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
	info_raio.write("Inicio: " + inicio_info + "\n")
	info_raio.write("Final: " + final_info + "\n")
	info_raio.close()


#Função de aplicação do Controlador
def Controle():
	cX1 = 0
	cX2 = 0
	eX1 = 0
	eX2 = 0
	cY1 = 0
	cY2 = 0
	eY1 = 0
	eY2 = 0
	
	while True:
		inicio = time.perf_counter()
		
		eX, eY, r = Cam.Rastreamento()
		eX = eX*(-1)
		
		cX = cX1*1.108-cX2*0.1088+eX*0.05322-eX1*0.04188+eX2*0.01001
		cX2 = cX1
		cX1 = cX
		eX2 = eX1
		eX1 = eX
		
		cY = cY1*1.117-cY2*0.1168+eY*0.04809-eY1*0.03559+eY2*0.008265
		cY2 = cY1
		cY1 = cY
		eY2 = eY1
		eY1 = eY
	
		#Movimentação dos Motores
		MoverMotores(cX, 0)
		
		if cv.waitKey != -1: break
		
		while time.perf_counter() - inicio < def_amostragem: pass
		
		if (time.perf_counter() - inicio) > 0.045 : print("Erro! Tempo de amostragem excedido: %s" %(time.perf_counter() - inicio))


	

			   #MAIN CODE		



Cam = Imagem(def_camera) #inicializa camera
modo = 0 #Inicializa com o modo de ajuste da máscara

#Inicialização do Arduino
arduino = serial.Serial('COM'+str(def_com), 9600)
print("Inicializando comunicação...")
time.sleep(2)
AjustaMotores()



while True:
	#Modo de ajuste de máscara
	while modo == 0:
		Cam.AjusteMascara()
		tecla = cv.waitKey(1)
		if tecla == ord('z'):
			Cam.PreConfig(1)
		if tecla == ord('x'):
			Cam.PreConfig(2)
		if tecla == ord('c'):
			Cam.PreConfig(3)
		if tecla == ord('v'):
			Cam.PreConfig(4)
		if tecla == ord('w'):
			MoverMotores(0, 1)
		if tecla == ord('s'):
			MoverMotores(0, -1)
		if tecla == ord('a'):
			MoverMotores(1, 0)
		if tecla == ord('d'):
			MoverMotores(-1, 0)
		if tecla != -1:
			break
	#Modo com controle aplicado
	while modo == 1:
		inicio = time.perf_counter()
		Controle()
		tecla = cv.waitKey(1)		
		if tecla != -1:
			break
		while(time.perf_counter()-inicio < def_amostragem):
			pass

	#Leitura de Teclas
	if tecla == 27: #Tecla ESC
		del Cam
		break
	#Seleção de Modos
	if tecla == ord('q'):
		cv.destroyAllWindows()
		modo = 0
	if tecla == ord('e'):
		cv.destroyAllWindows()
		modo = 1
	#Modo captura de Dados
	if tecla == ord('1'):
		EnsaioIdentX()
		time.sleep(4)
		EnsaioIdentY()
