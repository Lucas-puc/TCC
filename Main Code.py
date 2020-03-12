#Importando as bibliotecas necessárias
import cv2 as cv
import numpy as np
import time
import imutils
import serial








###################################Inicio da função de controle ######################################################################################################

#Posição inicial dos servos
angulo_X = 90
angulo_Y = 90

def Controle(posX, posY, tamX, tamY):
    global angulo_X
    global angulo_Y

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

    return;

###################################Fim da função de controle##########################################################################################################


####### Função para mover motores
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
    print(mensagem)
    mensagem = str.encode(mensagem)
    #arduino.write(mensagem)
    return;

#####################################################







###############################################################    Controle Aplicado

def ControleAplicado():
    #Fecha as janelas abertas no momento
    cv.destroyAllWindows()
    #Crianto variáveis para evitar problemas
    fps = '0'

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
	    contornos = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
	    #Cálculo de FPS
	    fps = str(round((1/(time.time() - init)), 1))


###############################################################    Fim do Controle Aplicado







###############################################################    Coleta de Dados (Degrau)



def ColetaDados():
    global angulo_X
    global angulo_Y
    novo_angulo_X = angulo_X
    novo_angulo_Y = angulo_Y
    
    #Fecha as janelas abertas no momento
    cv.destroyAllWindows()
    #Crianto variáveis para evitar problemas
    fps = '0'
    teste_on = 0;
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
	    contornos = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
			    #Desenha cruz no centro do circulo
			    cv.line(frame, (int(x-raio/4), int(y)), (int(x+raio/4), int(y)), (0, 0, 255), 1)
			    cv.line(frame, (int(x), int(y-raio/4)), (int(x), int(y+raio/4)), (0, 0, 255), 1)

	    erro_X = x - largura/2
	    erro_Y = y - altura/2

	    

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
	    if teste_on == 0:
		    #Mover para cima (w)
		    if tecla == 119:
			    angulo_X = angulo_X + 1
			    MoverMotores()
		    #Mover para baixo(s)
		    if tecla == 115:
			    angulo_X = angulo_X - 1
			    MoverMotores()
		    #Mover para esquerda (a)
		    if tecla == 97:
			    angulo_Y = angulo_Y - 1
			    MoverMotores()
		    #Mover para direita (d)
		    if tecla == 100:
			    angulo_Y = angulo_Y + 1
			    MoverMotores()
		    #Apertas "g" para começar a coleta de dados (escolhe direção usando w,a,s,d)
		    if tecla == 103:
			    teste_on = 1
			    tecla == cv.waitKey()
			    inicio_captura = 0
			    print("N:Tempo:Angulo X:Erro X:Angulo Y:Erro Y")
			    #Mover para cima (w)
			    if tecla == 119:
				    novo_angulo_X = angulo_X + 10
			    #Mover para baixo(s)
			    if tecla == 115:
				    novo_angulo_X = angulo_X - 10
			    #Mover para esquerda (a)
			    if tecla == 97:
				    novo_angulo_Y = angulo_Y - 10
			    #Mover para direita (d)
			    if tecla == 100:
				    novo_angulo_Y = angulo_Y + 10
			    
			
	    #Garante o intervalo de tempo constante
	    while (time.time() - init) < 1/30:
		    pass
   
	    #Cálculo de FPS
	    fps = str(round((1/(time.time() - init)), 1))

	    #Contagem de ciclos após iniciar a captura
	    if teste_on == 1:
		    print(str(time.time() - init) + ":" + str(angulo_X) + ":" + str(erro_X) + ":" + str(angulo_Y) + ":" + str(erro_Y))
		    #aplicação do degrau
		    if inicio_captura == 60:
			    angulo_X = novo_angulo_X
			    angulo_Y = novo_angulo_Y
			    MoverMotores()
		    if inicio_captura == 210:
			    teste_on = 0
		    inicio_captura = inicio_captura+1




#############################################################################    Fim Coleta de Dados











############################################################################   Menu e configuração



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

#Imagem com comandos
comandosImg = cv.imread('comandos.jpg')

#Loop principal
while True:
	#Printa imagem com comandos
	cv.imshow('Comandos', comandosImg)

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
	#Tecla "q" começa o controle aplicado
	if tecla == 113:
		ControleAplicado()
	#Tecla "w" começa o modo de coleta de dados
	if tecla == 119:
		ColetaDados()
	#Tecla "1" carrega a pre-configuração 1 (verde):
	if tecla == 49:
		cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 29)
		cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 86)
		cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 6)
		cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
		cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
		cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
	#Tecla "1" carrega a pre-configuração 2 (pele Lucas):
	if tecla == 50:
		cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 0)
		cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 65)
		cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 43)
		cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 21)
		cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
		cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)
	#Tecla "1" carrega a pre-configuração 3 (TBD):
	if tecla == 51:
		cv.setTrackbarPos("Min-H", "Ajuste de Mascara", 29)
		cv.setTrackbarPos("Min-S", "Ajuste de Mascara", 86)
		cv.setTrackbarPos("Min-V", "Ajuste de Mascara", 6)
		cv.setTrackbarPos("Max-H", "Ajuste de Mascara", 64)
		cv.setTrackbarPos("Max-S", "Ajuste de Mascara", 255)
		cv.setTrackbarPos("Max-V", "Ajuste de Mascara", 255)

#Libera a utilização da câmera
camera.release()

#Fecha todas as janelas do OpenCV
cv.destroyAllWindows()

