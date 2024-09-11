
# Controle de Mouse com a CÃ¢mera

Este projeto implementa um mouse virtual controlado por gestos usando a cÃ¢mera, com detecÃ§Ã£o de mÃ£os via [MediaPipe](https://google.github.io/mediapipe/). Com esse sistema, vocÃª pode mover o cursor e executar cliques de mouse com base nos movimentos e gestos das mÃ£os.

## Requisitos

Instale as dependÃªncias necessÃ¡rias executando os comandos abaixo:

```bash
pip install mediapipe
pip install pyautogui
pip install pygame
```

## Como Usar

1. Conecte sua cÃ¢mera e execute o arquivo `main.py`.
2. Para movimentar o mouse, posicione sua mÃ£o Ã  frente da cÃ¢mera.

### Gestos DisponÃ­veis

- **Clique esquerdo**: Junte o dedo indicador com o polegar.
- **Clique direito**: Junte o dedo mÃ©dio com o polegar.
- **Segurar botÃ£o (arrastar)**: Junte o dedo indicador e o mÃ©dio com o polegar (recomendado juntar o indicador primeiro).

## Arquitetura

O projeto utiliza as seguintes bibliotecas:

- **MediaPipe**: Para detectar e rastrear os landmarks da mÃ£o.
- **PyAutoGUI**: Para simular o movimento e cliques do mouse.
- **OpenCV**: Para capturar e processar as imagens da cÃ¢mera.

## Como Executar o Projeto

1. Clone o repositÃ³rio:

```bash
git clone https://github.com/VictorAraki/mouse_hand_tcc.git
cd mouse_hand_tcc
```

2. Instale as dependÃªncias mencionadas na seÃ§Ã£o de requisitos.
3. Execute o projeto com o seguinte comando:

```bash
python main.py
```

4. Para sair, pressione a tecla `Esc`.
