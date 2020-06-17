import ObjCamera as Camera
import ObjArduino as Arduino
import ObjControle as Controle

cam = Camera.Imagem(0)
ino = Arduino.Comando(6, 9600)
controle = Controle.Controle(cam, ino, 0.04)

cor = 1

print("Menu:\n1 - Controle Regulatório\n2 - Muda de Cor\n7 - Coleta em Controle Regulatório\n8 - Coleta em Malha Aberta"
      "\n9 - Coleta em Malha Fechada\nw,a,s,d - Mover\nPressione qualquer tecla para sair do regime atual.")


while True:

    cam.ajuste_mascara()

    if cam.tecla_pressionada() == ord('1'):
        controle.regulatorio(0)
        Camera.fechar_janelas()

    if cam.tecla_pressionada() == ord('2'):
        cor += 1
        if cor > 4:
            cor = 1
        cam.pre_config(cor)

    if cam.tecla_pressionada() == ord('3'):
        controle.regulatorio_grafico(0)
        Camera.fechar_janelas()

    if cam.tecla_pressionada() == ord('7'):
        controle.ensaios_regulatorio()
        Camera.fechar_janelas()

    if cam.tecla_pressionada() == ord('8'):
        controle.ensaios_indent()
        Camera.fechar_janelas()

    if cam.tecla_pressionada() == ord('9'):
        controle.ensaios_controlador()
        Camera.fechar_janelas()

    if cam.tecla_pressionada() in (ord('w'), ord('a'), ord('s'), ord('d')):
        ino.wasd(cam.tecla_pressionada())
        print("Mover")

    if cam.tecla_pressionada() == 27:  # ESC
        break

del cam
del ino
del controle
print("Processos finalizados.")
