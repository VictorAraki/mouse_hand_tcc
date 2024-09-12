import os

def set_env_var():
    """
    Configura todas as variaveis de ambiente, util para alterar pontos de interesse e sensibilidade do mouse
    """
    os.environ['MousePointerPoint'] = '9' # Integer, ponto da mao que sera usado como ponteiro do mouse
    os.environ['MouseSensibility_X'] = '1.5' # Float, sensibilidade da escala da tela em X
    os.environ['MouseSensibility_Y'] = '1.5' # Float, sensibilidade da escala da tela em Y
    os.environ['ScreenOffSet_width'] = '0.2' # Float, off_set da tela em X para poder alcançar o lado esquerdo
    os.environ['ScreenOffSet_height'] = '0.3' # Float, off_set da tela em Y para poder alcançar o lado superior
    
    os.environ['MouseReference'] = '4' # Integer, ponto da mao que sera usado como ref para o click
    os.environ['MouseClickRef'] = '8' # Integer, ponto da mao que se aproximada da ref gerara o click
    os.environ['DistanciaClick'] = '50' # Integer, valor em pixels para considerar um click
    os.environ['DurationMove'] = '0' # Float, duracao do movimento, quanto menor, mais rapido a atualizacao
