import cv2
import numpy as np

# Calcula a Normalized Cross-Correlation (NCC) entre duas imagens.
def calculate_ncc(imagem1, imagem2):

    # Converter a imagem para tons cinza
    imagem1_gray = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
    imagem2_gray = cv2.cvtColor(imagem2, cv2.COLOR_BGR2GRAY)

    # Verificar se as imagens possuem o mesmo tamanho
    if imagem1_gray.shape != imagem2_gray.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")

    # Calcular a media e o desvio padrao de cada imagem
    mean1, stddev1 = cv2.meanStdDev(imagem1_gray)
    mean2, stddev2 = cv2.meanStdDev(imagem2_gray)

    # Normalizam as imagens
    imagem1_normalized = (imagem1_gray - mean1) / stddev1
    imagem2_normalized = (imagem2_gray - mean2) / stddev2

    # Calcular o NCC
    ncc = np.mean(imagem1_normalized * imagem2_normalized)
    return ncc

    # Calcula a velocidade mEdia.

def calcular_velocidade_media(distancia, tempo):

    if tempo <= 0:
        raise ValueError("O tempo precisa ser maior que zero")
    velocidade_media_m_s = distancia / tempo
    velocidade_media_km_h = velocidade_media_m_s * 3.6
    return velocidade_media_m_s, velocidade_media_km_h

# Carregar as imagens
imagem1 = cv2.imread('Midia/IMAGEM_A.jpeg')
imagem2 = cv2.imread('Midia/IMAGEM_B.jpeg')

# Calcular o NCC entre as imagens
ncc_value = calculate_ncc(imagem1, imagem2)
print(f"Cross-Correlation: {ncc_value}")

# Insira a distância percorrida e tempo gasto
distancia_percorrida = float(input("Digite a distância percorrida em metros: "))
tempo_gasto = float(input("Digite o tempo gasto em segundos: "))

# Calcular a velocidade média
try:
    velocidade_media_m_s, velocidade_media_km_h = calcular_velocidade_media(distancia_percorrida, tempo_gasto)
    print(f"Velocidade média: {velocidade_media_m_s} metros por segundo")
    print(f"Velocidade média: {velocidade_media_km_h} quilômetros por hora")
except ValueError as e:
    print(f"Erro ao calcular velocidade média: {e}")
