import cv2
import numpy as np
import argparse
from moviepy.editor import VideoFileClip

# Função para processar vídeo
def process_video(input_file, output_file):
    # Carregar o vídeo
    video = VideoFileClip(input_file)
    
    # Aplicar uma transformação simples - neste caso, rotacionar o vídeo em 90 graus
    rotated_video = video.rotate(90)
    
    # Salvar o vídeo processado
    rotated_video.write_videofile(output_file, codec='libx264')

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

# Calcula a velocidade média.
def calcular_velocidade_media(distancia, tempo):
    if tempo <= 0:
        raise ValueError("O tempo precisa ser maior que zero")
    velocidade_media_m_s = distancia / tempo
    velocidade_media_km_h = velocidade_media_m_s * 3.6
    return velocidade_media_m_s, velocidade_media_km_h

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Processamento de vídeo e imagens')
    parser.add_argument('--video', required=True, help='Caminho para o arquivo de vídeo (.mp4)')
    parser.add_argument('--output_video', required=True, help='Caminho para salvar o vídeo processado')
    parser.add_argument('--image1', required=True, help='Caminho para a primeira imagem (.jpeg)')
    parser.add_argument('--image2', required=True, help='Caminho para a segunda imagem (.jpeg)')
    parser.add_argument('--distancia', type=float, required=True, help='Distância percorrida em metros')
    parser.add_argument('--tempo', type=float, required=True, help='Tempo gasto em segundos')
    
    args = parser.parse_args()

    # Carregar as imagens
    imagem1 = cv2.imread(args.image1)
    imagem2 = cv2.imread(args.image2)

    # Calcular o NCC entre as imagens
    ncc_value = calculate_ncc(imagem1, imagem2)
    print(f"Cross-Correlation: {ncc_value}")

    # Calcular a velocidade média
    try:
        velocidade_media_m_s, velocidade_media_km_h = calcular_velocidade_media(args.distancia, args.tempo)
        print(f"Velocidade média: {velocidade_media_m_s} metros por segundo")
        print(f"Velocidade média: {velocidade_media_km_h} quilômetros por hora")
    except ValueError as e:
        print(f"Erro ao calcular velocidade média: {e}")

    # Processar o vídeo
    process_video(args.video, args.output_video)

if __name__ == "__main__":
    main()
