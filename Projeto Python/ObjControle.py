import time
from datetime import datetime
import ObjCamera as Camera
import Plot_grafico as Grafico

# noinspection PyTypeChecker
class Controle:
    def __init__(self, cam, ino, def_amostragem):
        self.c_x1 = 0
        self.e_x1 = 0
        self.c_y1 = 0
        self.e_y1 = 0
        self.c_y2 = 0
        self.e_y2 = 0
        self.c_x2 = 0
        self.e_x2 = 0
        self.e_x = 0
        self.e_y = 0
        self.c_x = 0
        self.c_y = 0
        self.cam = cam
        self.ino = ino
        self.def_amostragem = def_amostragem

    def controle_x(self):
        self.c_x = 0.064557*self.e_x - 0.03577*self.e_x1 + 0.005091*self.e_x2 + 0.6037*self.c_x1 + 0.3963*self.c_x2
        self.c_x2 = self.c_x1
        self.e_x2 = self.e_x1
        self.c_x1 = self.c_x
        self.e_x1 = self.e_x

    def controle_y(self):
        self.c_y = 0.06183*self.e_y - 0.07155*self.e_y1 + 0.02935*self.e_y2 + 1.061*self.c_y1 - 0.06056*self.c_y2
        self.c_y2 = self.c_y1
        self.e_y2 = self.e_y1
        self.c_y1 = self.c_y
        self.e_y1 = self.e_y

    def zerar(self):
        self.c_x2 = 0
        self.e_x2 = 0
        self.c_y2 = 0
        self.e_y2 = 0
        self.c_x1 = 0
        self.e_x1 = 0
        self.c_y1 = 0
        self.e_y1 = 0
        self.e_x = 0
        self.e_y = 0

    def regulatorio(self, periodo):
        Camera.fechar_janelas()
        self.zerar()
        print("Iniciando controle regulatorio...")
        time.sleep(1)
        angulo_inicial_x, angulo_inicial_y = self.ino.atual()
        timer = time.perf_counter()
        while True:
            inicio = time.perf_counter()

            p_x, p_y, r = self.cam.rastreamento()

            self.e_x = p_x * (-1)
            self.e_y = p_y * (-1)

            if r > 0:
                self.controle_x()
                self.controle_y()

                # Envia sinal de controle para o atuador
                angulo_x = angulo_inicial_x + self.c_x
                angulo_y = angulo_inicial_y + self.c_y

                self.ino.mover(angulo_x, angulo_y)

            if self.cam.tecla_pressionada() != -1 and self.cam.tecla_pressionada() != ord('1'):
                break

            if self.cam.tecla_pressionada() == ord('1'):
                self.zerar()

            while (time.perf_counter() - inicio) < self.def_amostragem:
                pass

            if (time.perf_counter() - inicio) > 0.045:
                print("Erro! Tempo de amostragem excedido: %s" % (time.perf_counter() - inicio))

            if (time.perf_counter() - timer) > periodo > 0:
                break

    def ensaios_indent(self):

        # ENSAIO DO EIXO x

        Camera.fechar_janelas()
        print("Inicializando processo automatizado de coleta de dados - Eixo X")
        agora = datetime.now()
        inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Inicio: " + inicio_info)

        # Importando sinal de degrau
        entrada_txt = "Entrada/Degrau.txt"
        sinal = open(entrada_txt, "r")
        nz = len(sinal.readlines())
        u = [0] * nz
        value = [0] * nz
        sinal = open(entrada_txt, "r")
        k = 0
        for line in sinal:
            u[k] = float(line.rstrip())
            k += 1
        sinal.close()
        _, _, raio_inicio = self.cam.rastreamento()

        # Processo no eixo X
        print("Camera centralizada. Iniciando processo de ensaios para o eixo X.")

        for m in range(0, 100):
            tudo_certo = False
            print("Ensaio numero " + str(m))
            while not tudo_certo:
                self.centraliza(3)
                inicio_x, _, _ = self.cam.rastreamento()
                angulo_x_inicial, angulo_y_inicial = self.ino.atual()
                aux = 1
                if m % 2 == 0:
                    aux = -1
                if m < 50:
                    aux = -1
                if m < 25:
                    aux = 1
                tudo_certo = True

                for n in range(nz):
                    inicio = time.perf_counter()
                    self.ino.mover(angulo_x_inicial + aux * u[n], angulo_y_inicial)
                    value[n], _, _ = self.cam.rastreamento()
                    while time.perf_counter() - inicio < self.def_amostragem:
                        pass
                    if (time.perf_counter() - inicio) > 0.045:
                        print("Erro! Tempo de amostragem excedido: %s" % (time.perf_counter() - inicio))
                        tudo_certo = False

                if not tudo_certo:
                    print("Repetindo ensaio numero " + str(m))

                saida_txt = "Saida/X/Saida" + str(m + 1) + ".txt"
                resposta = open(saida_txt, "w")

                for k in range(nz):
                    resposta.write(str((value[k] - inicio_x)) + "\n")

                resposta.close()
                self.centraliza(3)

        print("Processo de coleta finalizado.")
        agora = datetime.now()
        final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Final: " + final_info)
        raio_txt = "Saida/X/Info Ensaio.txt"
        info_raio = open(raio_txt, "w")
        info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo X\n")
        info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
        info_raio.write("Inicio: " + inicio_info + "\n")
        info_raio.write("Final: " + final_info + "\n")
        info_raio.close()

        # ENSAIO DO EIXO Y

        Camera.fechar_janelas()
        print("Inicializando processo automatizado de coleta de dados - Eixo Y")
        agora = datetime.now()
        inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Inicio: " + inicio_info)

        # Importando sinal de degrau
        entrada_txt = "Entrada/Degrau.txt"
        sinal = open(entrada_txt, "r")
        nz = len(sinal.readlines())
        u = [0] * nz
        value = [0] * nz
        sinal = open(entrada_txt, "r")
        k = 0
        for line in sinal:
            u[k] = float(line.rstrip())
            k += 1
        sinal.close()
        _, _, raio_inicio = self.cam.rastreamento()

        # Processo no eixo Y
        print("Camera centralizada. Iniciando processo de ensaios para o eixo Y.")

        for m in range(0, 100):
            tudo_certo = False
            print("Ensaio numero " + str(m))
            while not tudo_certo:
                self.centraliza(8)
                _, inicio_y, _ = self.cam.rastreamento()
                angulo_x_inicial, angulo_y_inicial = self.ino.atual()
                aux = 1
                if m % 2 == 0:
                    aux = -1
                if m < 50:
                    aux = -1
                if m < 25:
                    aux = 1
                tudo_certo = True

                for n in range(nz):
                    inicio = time.perf_counter()
                    self.ino.mover(angulo_x_inicial, angulo_y_inicial + aux * u[n])
                    _, value[n], _ = self.cam.rastreamento()
                    while time.perf_counter() - inicio < self.def_amostragem:
                        pass
                    if (time.perf_counter() - inicio) > 0.045:
                        print("Erro! Tempo de amostragem excedido: %s" % (time.perf_counter() - inicio))
                        tudo_certo = False

                if not tudo_certo:
                    print("Repetindo ensaio numero " + str(m))

                saida_txt = "Saida/Y/Saida" + str(m + 1) + ".txt"
                resposta = open(saida_txt, "w")

                for k in range(nz):
                    resposta.write(str((value[k] - inicio_y)) + "\n")

                resposta.close()
                self.centraliza(8)

        print("Processo de coleta finalizado.")
        agora = datetime.now()
        final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Final: " + final_info)
        raio_txt = "Saida/Y/Info Ensaio.txt"
        info_raio = open(raio_txt, "w")
        info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo Y\n")
        info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
        info_raio.write("Inicio: " + inicio_info + "\n")
        info_raio.write("Final: " + final_info + "\n")
        info_raio.close()

    def ensaios_controlador(self):

        # ENSAIO DO EIXO x

        Camera.fechar_janelas()
        print("Inicializando processo automatizado de coleta de dados - Eixo X")
        agora = datetime.now()
        inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Inicio: " + inicio_info)

        # Importando sinal de degrau
        entrada_txt = "Validação/U.txt"
        sinal = open(entrada_txt, "r")
        nz = len(sinal.readlines())
        u = [0] * nz
        value = [0] * nz
        ctrl = [None] * nz
        sinal = open(entrada_txt, "r")
        k = 0
        for line in sinal:
            u[k] = float(line.rstrip())
            k += 1
        sinal.close()
        _, _, raio_inicio = self.cam.rastreamento()

        # Processo no eixo X
        print("Camera centralizada. Iniciando processo de ensaios para o eixo X.")

        for m in range(0, 100):
            tudo_certo = False
            print("Ensaio numero " + str(m))
            while not tudo_certo:
                self.centraliza(3)
                inicio_x, _, _ = self.cam.rastreamento()
                angulo_x_inicial, angulo_y_inicial = self.ino.atual()
                aux = 1
                if m % 2 == 0:
                    aux = -1
                if m < 50:
                    aux = -1
                if m < 25:
                    aux = 1
                tudo_certo = True
                self.zerar()

                for n in range(nz):
                    inicio = time.perf_counter()
                    value[n], _, _ = self.cam.rastreamento()
                    self.e_x = aux * u[n] - value[n]
                    self.controle_x()
                    self.ino.mover(angulo_x_inicial + self.c_x, angulo_y_inicial)
                    ctrl[n] = self.c_x
                    while time.perf_counter() - inicio < self.def_amostragem:
                        pass
                    if (time.perf_counter() - inicio) > 0.045:
                        print("Erro! Tempo de amostragem excedido: %s" % (time.perf_counter() - inicio))
                        tudo_certo = False

                if not tudo_certo:
                    print("Repetindo ensaio numero " + str(m))

                saida_txt = "Validação/X/Saida" + str(m + 1) + ".txt"
                resposta = open(saida_txt, "w")
                for k in range(nz):
                    resposta.write(str((value[k] - inicio_x)) + "\n")
                resposta.close()

                ctrl_txt = "Validação/X/Controle" + str(m + 1) + ".txt"
                resposta = open(ctrl_txt, "w")
                for k in range(nz):
                    resposta.write(str(ctrl[k]) + "\n")
                resposta.close()

                self.centraliza(3)

        print("Processo de coleta finalizado.")
        agora = datetime.now()
        final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Final: " + final_info)
        raio_txt = "Validação/X/Info Ensaio.txt"
        info_raio = open(raio_txt, "w")
        info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo X\n")
        info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
        info_raio.write("Inicio: " + inicio_info + "\n")
        info_raio.write("Final: " + final_info + "\n")
        info_raio.close()

        # ENSAIO DO EIXO Y

        Camera.fechar_janelas()
        print("Inicializando processo automatizado de coleta de dados - Eixo Y")
        agora = datetime.now()
        inicio_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Inicio: " + inicio_info)

        # Importando sinal de degrau
        entrada_txt = "Validação/U.txt"
        sinal = open(entrada_txt, "r")
        nz = len(sinal.readlines())
        u = [0] * nz
        value = [0] * nz
        ctrl = [None] * nz
        sinal = open(entrada_txt, "r")
        k = 0
        for line in sinal:
            u[k] = float(line.rstrip())
            k += 1
        sinal.close()
        _, _, raio_inicio = self.cam.rastreamento()

        # Processo no eixo Y
        print("Camera centralizada. Iniciando processo de ensaios para o eixo Y.")

        for m in range(0, 100):
            tudo_certo = False
            print("Ensaio numero " + str(m))
            while not tudo_certo:
                self.centraliza(8)
                _, inicio_y, _ = self.cam.rastreamento()
                angulo_x_inicial, angulo_y_inicial = self.ino.atual()
                aux = 1
                if m % 2 == 0:
                    aux = -1
                if m < 50:
                    aux = -1
                if m < 25:
                    aux = 1
                tudo_certo = True
                self.zerar()

                for n in range(nz):
                    inicio = time.perf_counter()
                    _, value[n], _ = self.cam.rastreamento()
                    self.e_y = aux * u[n] - value[n]
                    self.controle_y()
                    self.ino.mover(angulo_x_inicial, angulo_y_inicial + self.c_y)
                    ctrl[n] = self.c_y
                    while time.perf_counter() - inicio < self.def_amostragem:
                        pass
                    if (time.perf_counter() - inicio) > 0.045:
                        print("Erro! Tempo de amostragem excedido: %s" % (time.perf_counter() - inicio))
                        tudo_certo = False

                if not tudo_certo:
                    print("Repetindo ensaio numero " + str(m))

                saida_txt = "Validação/Y/Saida" + str(m + 1) + ".txt"
                resposta = open(saida_txt, "w")
                for k in range(nz):
                    resposta.write(str((value[k] - inicio_y)) + "\n")
                resposta.close()

                ctrl_txt = "Validação/Y/Controle" + str(m + 1) + ".txt"
                resposta = open(ctrl_txt, "w")
                for k in range(nz):
                    resposta.write(str(ctrl[k]) + "\n")
                resposta.close()

                self.centraliza(8)

        print("Processo de coleta finalizado.")
        agora = datetime.now()
        final_info = agora.strftime("%d,%m,%Y %H;%M;%S")
        print("Final: " + final_info)
        raio_txt = "Validação/Y/Info Ensaio.txt"
        info_raio = open(raio_txt, "w")
        info_raio.write("Ensaio de coleta de resposta ao degrau para o eixo Y\n")
        info_raio.write("Raio (pixels): " + str(raio_inicio) + "\n")
        info_raio.write("Inicio: " + inicio_info + "\n")
        info_raio.write("Final: " + final_info + "\n")
        info_raio.close()

    def centraliza(self, tolerancia):
        print("Centralizando...")
        x, y, _ = self.cam.rastreamento()
        while (abs(x) > tolerancia) or (abs(y) > tolerancia):
            print("x" + str(abs(x)) + ":y" + str(abs(y)) + ":t" + str(tolerancia))
            self.regulatorio(3)
            time.sleep(1)
            x, y, _ = self.cam.rastreamento()
        print("Centralizado")

    def ensaios_regulatorio(self):
        self.centraliza(4)
        print("Coletando Dados")
        nz = 250
        valor_pan = [0] * nz
        valor_tilt = [0] * nz
        controle_pan = [0] * nz
        controle_tilt = [0] * nz
        angulo_x_inicial, angulo_y_inicial = self.ino.atual()
        self.zerar()
        for n in range(nz):
            if n % 50 == 0:
                print("MOVE!!!")
            inicio = time.perf_counter()
            valor_pan[n], valor_tilt[n], _ = self.cam.rastreamento()
            self.e_x = -valor_pan[n]
            self.e_y = -valor_tilt[n]
            self.controle_x()
            self.controle_y()
            self.ino.mover(angulo_x_inicial + self.c_x, angulo_y_inicial + self.c_y)
            controle_pan[n] = self.c_x
            controle_tilt[n] = self.c_y
            while time.perf_counter() - inicio < self.def_amostragem:
                pass

        resposta = open("Coleta Regulatório/Saída Pan.txt", "w")
        for k in range(nz):
            resposta.write(str(valor_pan[k]) + "\n")
        resposta.close()

        resposta = open("Coleta Regulatório/Saída Tilt.txt", "w")
        for k in range(nz):
            resposta.write(str(valor_tilt[k]) + "\n")
        resposta.close()

        resposta = open("Coleta Regulatório/Controle Pan.txt", "w")
        for k in range(nz):
            resposta.write(str(controle_pan[k]) + "\n")
        resposta.close()

        resposta = open("Coleta Regulatório/Controle Tilt.txt", "w")
        for k in range(nz):
            resposta.write(str(controle_tilt[k]) + "\n")
        resposta.close()

        print("Processo de coleta finalizado.")

    def regulatorio_grafico(self, periodo):

        Camera.fechar_janelas()
        self.zerar()
        print("Iniciando controle regulatorio...")
        time.sleep(1)
        angulo_inicial_x, angulo_inicial_y = self.ino.atual()
        timer = time.perf_counter()

        # Create a plotter class object
        grafico = Grafico.Plotter(400, 400, 2)

        while True:
            inicio = time.perf_counter()

            p_x, p_y, r = self.cam.rastreamento()

            self.e_x = p_x * (-1)
            self.e_y = p_y * (-1)
            grafico.multiplot([int(p_x/2), int(p_y/2)])

            if r > 0:
                self.controle_x()
                self.controle_y()

                # Envia sinal de controle para o atuador
                angulo_x = angulo_inicial_x + self.c_x
                angulo_y = angulo_inicial_y + self.c_y

                self.ino.mover(angulo_x, angulo_y)

            if self.cam.tecla_pressionada() != -1 and self.cam.tecla_pressionada() != ord('1'):
                break

            if self.cam.tecla_pressionada() == ord('1'):
                self.zerar()

            while (time.perf_counter() - inicio) < self.def_amostragem:
                pass

            if (time.perf_counter() - timer) > periodo > 0:
                break
