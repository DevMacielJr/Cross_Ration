import cv2
import numpy as np
import os

# Calcula a Normalized Cross-Correlation (NCC) entre duas imagens.
def calculate_ncc(imagem1, imagem2):

    imagem1_gray = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
    imagem2_gray = cv2.cvtColor(imagem2, cv2.COLOR_BGR2GRAY)

    if imagem1_gray.shape != imagem2_gray.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")

    mean1, stddev1 = cv2.meanStdDev(imagem1_gray)
    mean2, stddev2 = cv2.meanStdDev(imagem2_gray)

    mean1, stddev1 = mean1[0][0], stddev1[0][0]
    mean2, stddev2 = mean2[0][0], stddev2[0][0]

    imagem1_normalized = (imagem1_gray - mean1) / stddev1 if stddev1 != 0 else imagem1_gray - mean1
    imagem2_normalized = (imagem2_gray - mean2) / stddev2 if stddev2 != 0 else imagem2_gray - mean2

    ncc = np.mean(imagem1_normalized * imagem2_normalized)
    return ncc

# Calcula a velocidade media.
def calcular_velocidade_media(distancia, tempo):

    if tempo <= 0:
        raise ValueError("O tempo precisa ser maior que zero")
    velocidade_media_m_s = distancia / tempo
    velocidade_media_km_h = velocidade_media_m_s * 3.6
    return velocidade_media_m_s, velocidade_media_km_h

# Função para receber arquivo de video
def load_video(video_path):

    if not os.path.exists(video_path):  # Verifica se o arquivo de video existe
        raise ValueError("O arquivo de vídeo não existe. Verifique o caminho do arquivo.")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():  # Verifica se o video foi aberto corretamente
        raise ValueError("Erro ao abrir o vídeo. Verifique o caminho do arquivo.")
    return cap

# Função para extrair metadados basicos do video
def get_video_metadata(video_cap):

    fps = video_cap.get(cv2.CAP_PROP_FPS)
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    return {
        "FPS": fps,
        "Resolução": (width, height),
        "Duração (s)": duration,
        "Total de quadros": frame_count
    }

# Função para extrair frames especificos do video
def extract_frame(video_cap, frame_number):

    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number < 0 or frame_number >= total_frames:
        raise ValueError(f"O número do quadro deve estar entre 0 e {total_frames - 1}")

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video_cap.read()
    if not ret:
        raise ValueError("Erro ao ler o quadro do vídeo. Verifique o número do quadro.")
    return frame

# Função para sobrepor dois quadros em uma imagem
def overlay_images(imagemA, transparencyA, imagemB, transparencyB):
    if imagemA.shape != imagemB.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")
    overlay = cv2.addWeighted(imagemA, transparencyA, imagemB, transparencyB, 0)
    return overlay

# Testar as funções
def main():

    # Carregar as imagens
    imagem1 = cv2.imread('Midia/IMAGEM_A.jpeg')
    imagem2 = cv2.imread('Midia/IMAGEM_B.jpeg')

    if imagem1 is None or imagem2 is None:
        raise ValueError("Erro ao carregar as imagens. Verifique os caminhos dos arquivos.")

    # Calcular o NCC entre as imagens
    ncc_value = calculate_ncc(imagem1, imagem2)
    print(f"Cross-Correlation: {ncc_value}")

    distancia_percorrida = float(input("Digite a distância percorrida em metros: "))
    tempo_gasto = float(input("Digite o tempo gasto em segundos: "))

    try:
        velocidade_media_m_s, velocidade_media_km_h = calcular_velocidade_media(distancia_percorrida, tempo_gasto)
        print(f"Velocidade média: {velocidade_media_m_s} metros por segundo")
        print(f"Velocidade média: {velocidade_media_km_h} quilômetros por hora")
    except ValueError as e:
        print(f"Erro ao calcular velocidade média: {e}")

    # Caminho do video
    video_path = 'Midia/VIDEO.mp4'
    print(f"Verificando o caminho do vídeo: {video_path}")
    print(f"O arquivo existe? {os.path.exists(video_path)}")

    # Carregar o video
    try:
        video_cap = load_video(video_path)
    except ValueError as e:
        print(e)
        return

    # Obter metadados do video
    metadata = get_video_metadata(video_cap)
    print("Metadados do vídeo:", metadata)

    # Extrair frames especificos
    frame_number1 = 100
    frame_number2 = 200

    try:
        frame1 = extract_frame(video_cap, frame_number1)
        frame2 = extract_frame(video_cap, frame_number2)
    except ValueError as e:
        print(e)
        return

    # Sobrepor os frames
    overlay_image = overlay_images(frame1, 0.5, frame2, 0.5)

    # Mostrar a imagem sobreposta
    cv2.imshow('Overlay Image', overlay_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
