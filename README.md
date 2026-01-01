🖥️ Overlay Caótico em Pygame (Windows)

⚠️ AVISO IMPORTANTE
Este projeto não é uma aplicação comum. Ele foi feito para fins de teste, estudo, zoeira e caos controlado.
Ao executar, ele bloqueia o mouse, cria centenas/milhares de pastas no Desktop, toca áudios e exibe um overlay fullscreen impossível de fechar normalmente.

👉 NÃO execute em um PC importante.
👉 NÃO execute sem saber exatamente o que o código faz.

📌 O que esse projeto faz

Cria um overlay fullscreen sem bordas

Usa transparência real do Windows (ColorKey)

Exibe imagens centralizadas

Toca áudios em sequência

Mostra texto animado passando na tela

Faz o fundo piscar com cores aleatórias

Trava o mouse no centro da tela

Cria automaticamente:

1000 pastas no Desktop (configurável)

100 cópias de uma imagem dentro de cada pasta

Ignora:

ESC

Fechar janela

Só encerra após o tempo definido no código

🧠 Tecnologias usadas

Python 3.11+

Pygame

PyInstaller (para gerar .exe)

PyWin32 (controle de janela e transparência)

PyAutoGUI (travar o mouse)

Multithreading

📂 Estrutura de arquivos
projeto/
│
├── main.py
├── img1.png
├── img2.png
├── TOMA.png
├── audio.mp3
├── audio2.mp3
└── README.md


⚠️ Todos esses arquivos são obrigatórios, tanto no .py quanto no .exe.

⚙️ Configurações principais
🔥 Caos
QTD_PASTAS = 1000
TAMANHO_NOME = 10
INTERVALO = 0.01
DURACAO_ANIMACAO = 150

🎨 Visual
FPS = 60
COR_TRANSPARENTE = (255, 0, 255)
TAMANHO_FONTE = 49

📝 Texto animado
TEXTO_IMG2 = "TA SENDO ABUSADO PELA LEYLEY ..."

🪟 Transparência no Windows

O overlay usa Layered Window + ColorKey, fazendo o magenta (RGB(255,0,255)) virar transparente de verdade no Windows.

Isso permite:

Janela invisível

Elementos flutuando por cima de tudo

Sempre TOPMOST

🖱️ Travamento do mouse

O mouse é travado usando uma thread separada, que:

Move o cursor para o centro da tela

Atualiza a posição a cada 0.01s

Funciona mesmo durante animações e áudio

threading.Thread(target=travar_mouse, daemon=True).start()

🎵 Áudio

audio.mp3 toca primeiro

Após terminar, inicia audio2.mp3

O código espera o áudio terminar antes de continuar

🚨 Como ENCERRAR se algo der errado

Se você rodar isso sem querer:

Ctrl + Alt + Del

Abrir Gerenciador de Tarefas

Finalizar o processo:

main.exe ou python.exe

Se o mouse estiver travado:

Use teclado apenas

Navegue com Tab, Setas e Enter

📦 Gerar .exe

Com todos os arquivos na mesma pasta:

pyinstaller --onefile --noconsole main.py


⚠️ O .exe precisa dos arquivos:

imagens

áudios

Se quiser tudo embutido, tem que configurar --add-data.

🧪 Finalidade

Este projeto é voltado para:

Estudo de Pygame avançado

Manipulação de janelas no Windows

Threads em Python

Efeitos visuais extremos

Testes de comportamento do sistema

🛑 Responsabilidade

Você executa por sua conta e risco.
O autor não se responsabiliza por:

Perda de arquivos

Desktop poluído

Sustos

PCs travados

Questionamentos morais
