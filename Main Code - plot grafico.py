#Importando as bibliotecas necessárias
import cv2 as cv
import numpy as np
import time
import imutils
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


###################################Inicio da função de controle ######################################################################################################

#Variáveis globais
angulo_X = 45
angulo_Y = 45
erro_X = 0
erro_Y = 0

def Controle(posX, posY, tamX, tamY):
    global angulo_X
    global angulo_Y
    global erro_X
    global erro_Y

    #Calculo do erro
    erro_X = posX - tamX/2
    erro_Y = tamY/2 - posY

    #Aplica o controle
    controle_X = erro_X/100
    controle_Y = erro_Y/100

    #Ajusta a saída
    angulo_X = angulo_X - controle_X
    angulo_Y = angulo_Y - controle_Y

    #Saturação
    if angulo_X > 180 : angulo_X = 180 
    if angulo_X < 0 : angulo_X = 0 
    if angulo_Y > 180 : angulo_Y = 180 
    if angulo_Y < 0 : angulo_Y = 0 

    #Envia comando para o arduino
    mensagem = "X" + str(int(angulo_X)) + "Y" + str(int(angulo_Y))
    print(mensagem)
    mensagem = str.encode(mensagem)
    #arduino.write(mensagem)
    return;

###################################Fim da função de controle##########################################################################################################



tempo_vetor = np.linspace(0,15,450)
errox_vetor = [0]*450
#Função para plotar gráfico
def grafico(i):
    plt.cla()
    plt.plot(tempo_vetor, errox_vetor)
    plt.pause(0.05)







#Inicializa Camera. Define qual câmera usar: 0 = câmera integrada // 1 = câmera USB
camera = cv.VideoCapture(0) 


#Inicializa comunicação com o arduino
#arduino = serial.Serial('COM7', 9600, timeout = 1)


#Delay para aguardar a inicialização da câmera e do arduino
print("Inicializando...")
time.sleep(2)
print("Perifericos inicializados. Começando a exibição de vídeo")


#Criação da janela de ajuste de máscara 
def nada(x):
	#Quando alterar o valor de alguma trackbar 
	pass
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


#################Loop de ajuste
while True:
	#Captura o frame atual
	_, frame = camera.read() 

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

	cor_min = np.array([min_h, min_s, min_v])
	cor_max = np.array([max_h, max_s, max_v])
	mascara = cv.inRange(hsv, cor_min, cor_max)

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

	#Verificação de teclas pressionadas
	tecla = cv.waitKey(1)
	#Tecla "ESC" sai do loop
	if tecla == 27:
		break
	#Tecla "1" carrega a pre-configuração 1 (verde):
	if tecla == 49:
		cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 29)
		cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 86)
		cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 6)
		cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
		cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
		cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)

#Fecha as janelas abertas no momento
cv.destroyAllWindows()





############Código principal

#Crianto variáveis para evitar problemas
fps = '0'
erroXVetor = [0]*450
tempoVetor = np.linspace(0, 15, 450)

#Loop de trabalho
while True:
	init = time.time()
	#Captura o frame atual e salva o tamanho da imagem
	_, frame = camera.read()
	altura, largura,_ = frame.shape

	#Suavização da imagem para filtrar ruidos
	frame_suave = cv.GaussianBlur(frame, (11, 11), 0)
	
	#Converte para o color-space de BGR (RGB) para HSV (Hue-Saturation-Value)
	hsv = cv.cvtColor(frame_suave, cv.COLOR_BGR2HSV)

	#Criação da máscara de cor filtrando por parâmetros de HSV mínimos e máximos
	cor_min = np.array([min_h, min_s, min_v])
	cor_max = np.array([max_h, max_s, max_v])
	mascara = cv.inRange(hsv, cor_min, cor_max)

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
			#Função de controle
			Controle(x, y, largura, altura)                    
			#Desenha o circulo (cor em BGR)
			cv.circle(frame, (int(x), int(y)), int(raio), (0, 0, 255), 2)
			#Desenha cruz no centro do circulo
			cv.line(frame, (int(x-raio/4), int(y)), (int(x+raio/4), int(y)), (0, 0, 255), 1)
			cv.line(frame, (int(x), int(y-raio/4)), (int(x), int(y+raio/4)), (0, 0, 255), 1)

	#Desenha uma cruz no centro do frame
	cv.line(frame, (largura//2-10, altura//2), (largura//2+10, altura//2), (255, 0, 0), 1)
	cv.line(frame, (largura//2, altura//2-10), (largura//2, altura//2+10), (255, 0, 0), 1)
	
	#Escreve os frames por segundo
	cv.putText(frame, "FPS: " + fps, (0, altura-3), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255))
	
	#Mostra a imagem capturada da câmera e da máscara de cor
	cv.imshow("Camera", frame)	
 
	#Verificação de teclas pressionadas
	tecla = cv.waitKey(1)
	#Tecla "ESC" sai do loop
	if tecla == 27:
		break
	while (time.time() - init) < 1/30:
	    pass
	
	fps = str(round((1/(time.time() - init)), 1))

	ani = FuncAnimation(plt.gcf(),grafico, 1000)
	plt.tight_layout()
	plt.show()


#Libera a utilização da câmera
camera.release()

#Fecha todas as janelas do OpenCV
cv.destroyAllWindows()
	
