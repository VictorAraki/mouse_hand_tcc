
# Controle de Mouse com a Camera

Este projeto implementa um mouse virtual controlado por gestos usando a camera, com deteccao de maos via [MediaPipe](https://google.github.io/mediapipe/). Com esse sistema, voce pode mover o cursor e executar cliques de mouse com base nos movimentos e gestos das maos.

## Requisitos

Instale as dependencias necessarias executando os comandos abaixo:

```bash
pip install mediapipe
pip install pyautogui
pip install pygame
```

## Como Usar

1. Conecte sua camera e execute o arquivo `main.py`.
2. Para movimentar o mouse, posicione sua mao e  frente da camera.

### Gestos Disponi­veis

- **Clique esquerdo**: Junte o dedo indicador com o polegar.
- **Clique direito**: Junte o dedo medio com o polegar.
- **Segurar botao (arrastar)**: Junte o dedo indicador e o meio com o polegar (recomendado juntar o indicador primeiro).

## Arquitetura

O projeto utiliza as seguintes bibliotecas:

- **MediaPipe**: Para detectar e rastrear os landmarks da mao.
- **PyAutoGUI**: Para simular o movimento e cliques do mouse.
- **OpenCV**: Para capturar e processar as imagens da camera.

/projeto_mouse
    ├── interface.py        # Interface grafica e controle dos botoes
    ├── mouse_control.py    # Funcoes relacionadas a captura e controle de mao/mouse
    ├── utils.py            # Funcionalidades basicas como inicializacao da camera
    └── main.py             # Arquivo principal que conecta tudo
Como Funciona:
- **interface.py**: Responsavel pela interface grafica. Ele cria os botoes e chama as funcoes de controle de mouse em mouse_control.py.
- **mouse_control.py**: Contem as funcoes para processar os gestos e controlar o mouse.
- **utils.py**: Contem funcoes auxiliares como a inicializacao da camera e as configuracoes de deteccao.
## Como Executar o Projeto

1. Clone o repositorio:

```bash
git clone https://github.com/VictorAraki/mouse_hand_tcc.git
cd mouse_hand_tcc
```

2. Instale as dependencias mencionadas na sessao de requisitos.
3. Execute o projeto com o seguinte comando:

```bash
python main.py
```

4. Para sair, pressione a tecla `Esc`.

