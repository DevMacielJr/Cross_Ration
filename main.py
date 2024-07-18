import cv2
import numpy as np
import os

#_________________________ Calcula a Normalized Cross-Correlation (NCC) entre duas imagens. ________________________#

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

#___________________________________________ Calcula a velocidade média. ___________________________________________#

def calcular_velocidade_media(distancia, tempo):

    if tempo <= 0:
        raise ValueError("O tempo precisa ser maior que zero")
    velocidade_media_m_s = distancia / tempo
    velocidade_media_km_h = velocidade_media_m_s * 3.6
    return velocidade_media_m_s, velocidade_media_km_h

#______________________________________ Função para receber arquivo de vídeo. ______________________________________#

def load_video(video_path):

    if not os.path.exists(video_path):
        raise ValueError("O arquivo de vídeo não existe. Verifique o caminho do arquivo.")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Erro ao abrir o vídeo. Verifique o caminho do arquivo.")
    return cap

#_________________________________ Função para extrair metadados básicos do vídeo. _________________________________#

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

#________________________________ Função para extrair frames específicos do vídeo. _________________________________#

def extract_frame(video_cap, frame_number):

    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number < 0 or frame_number >= total_frames:
        raise ValueError(f"O número do quadro deve estar entre 0 e {total_frames - 1}")

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video_cap.read()
    if not ret:
        raise ValueError("Erro ao ler o quadro do vídeo. Verifique o número do quadro.")
    return frame

#_________________________________ Função para sobrepor dois quadros em uma imagem._________________________________#

def overlay_images(imagemA, transparencyA, imagemB, transparencyB):

    if imagemA.shape != imagemB.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")
    overlay = cv2.addWeighted(imagemA, transparencyA, imagemB, transparencyB, 0)
    return overlay

#_____________________________________ Função para salvar a imagem sobreposta. _____________________________________#

def save_image(image, output_path):

    cv2.imwrite(output_path, image)
    print(f"Imagem salva em: {output_path}")

#______________________________________ Função para adicionar texto à imagem. ______________________________________#

def add_text_to_image(image, text, position, font_scale=0.5, font_color=(0, 255, 255), font_thickness=1):

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

#___________________________ Função de callback para capturar clique de mouse na imagem. ___________________________#

def mouse_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clique detectado nas coordenadas (x, y): ({x}, {y})")
        param['clicked_point'] = (x, y)
        param['marked_points'].append((x, y))
        cv2.circle(param['image'], (x, y), 5, (0, 255, 255), -1)  # Marca o ponto clicado em amarelo na imagem

#______________________________________ Função para receber dados do veículo. ______________________________________#

def receber_dados_veiculo():

    marca = input("Digite a marca do veículo: ")
    modelo = input("Digite o modelo do veículo: ")
    cor = input("Digite a cor do veículo: ")
    tamanho_entre_eixos = float(input("Digite o tamanho do entre-eixos do veículo (em metros): "))
    return marca, modelo, cor, tamanho_entre_eixos


#__________________________________ Função para calcular a relação pixels/metros. __________________________________#

def calcular_relacao_pixels_metros(pontos_marcados, distancia_real_metros):
    if len(pontos_marcados) != 4:
        raise ValueError("É necessário marcar exatamente 4 pontos (T1, D1, T2, D2)")

    # Extrair os pontos marcados
    T1, D1, T2, D2 = pontos_marcados

    # Calcular as distâncias em pixels entre os pontos
    distancia_pixels_T1_D1 = calculate_distance(T1[0], T1[1], D1[0], D1[1])
    distancia_pixels_T2_D2 = calculate_distance(T2[0], T2[1], D2[0], D2[1])

    # Calcular a relação pixels/metros para cada eixo (x e y)
    relacao_pixels_metros_x = distancia_real_metros / ((distancia_pixels_T1_D1 + distancia_pixels_T2_D2) / 2)
    relacao_pixels_metros_y = relacao_pixels_metros_x  # Supondo uma relação uniforme

    return relacao_pixels_metros_x, relacao_pixels_metros_y


#__________________________________ Função para pintar a imagem T1, D1, T2 E D2. __________________________________#

def paint_on_image(image, image_name, marked_points):

    cv2.imshow(image_name, image)
    print("Pinte círculos amarelos nos pontos desejados (T1, D1, T2, D2). Pressione 'Esc' para terminar e continuar.")
    mouse_params = {'image_name': image_name, 'image': image, 'marked_points': marked_points}
    cv2.setMouseCallback(image_name, mouse_click, mouse_params)
    while True:
        cv2.imshow(image_name, image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Pressione 'Esc' para sair
            break
    cv2.destroyAllWindows()
    return marked_points

#__________________________________ Função para calcular a distância dos pontos. __________________________________#

def calculate_distance(x1, y1, x2, y2):

    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#________________________________________________ Função principal ________________________________________________#

def main():

    # Solicitar os caminhos das imagens e do vídeo
    image_path1 = input("Digite o caminho da primeira imagem: ")
    image_path2 = input("Digite o caminho da segunda imagem: ")
    video_path = input("Digite o caminho do vídeo: ")

    # Carregar as imagens
    imagem1 = cv2.imread(image_path1)
    imagem2 = cv2.imread(image_path2)

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

    # Receber dados do veículo
    marca, modelo, cor, tamanho_entre_eixos = receber_dados_veiculo()
    print(f"Dados do veículo: Marca: {marca}, Modelo: {modelo}, Cor: {cor}, Tamanho entre eixos: {tamanho_entre_eixos} metros")

    # Configurar callback para captura de clique de mouse
    cv2.namedWindow('Imagem Sobreposta')
    mouse_params = {'clicked_point': None, 'marked_points': []}
    cv2.setMouseCallback('Imagem Sobreposta', mouse_click, mouse_params)

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
    frame_number1 = 17
    frame_number2 = 20

    try:
        frame1 = extract_frame(video_cap, frame_number1)
        frame2 = extract_frame(video_cap, frame_number2)
    except ValueError as e:
        print(e)
        return

    # Sobrepor os frames
    try:
        overlay_image = overlay_images(frame1, 0.5, frame2, 0.5)
    except ValueError as e:
        print(e)
        return

    # Adicionar texto à imagem sobreposta
    metadata_text = f"FPS: {metadata['FPS']}, Resolução: {metadata['Resolução'][0]}x{metadata['Resolução'][1]}, Duração: {metadata['Duração (s)']:.2f}s, Total de quadros: {metadata['Total de quadros']}"
    results_text = f"NCC: {ncc_value:.2f}, Velocidade média: {velocidade_media_m_s:.2f} m/s ({velocidade_media_km_h:.2f} km/h)"
    combined_text = metadata_text + " | " + results_text

    text_position = (10, overlay_image.shape[0] - 10)
    add_text_to_image(overlay_image, combined_text, text_position)

    # Pintar na imagem
    markers = ['T1', 'D1', 'T2', 'D2']
    paint_on_image(overlay_image.copy(), 'Imagem Sobreposta', mouse_params['marked_points'])

    # Mostrar a imagem sobreposta com os pontos marcados
    for point, marker in zip(mouse_params['marked_points'], markers):
        cv2.putText(overlay_image, marker, (point[0], point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.circle(overlay_image, (point[0], point[1]), 5, (0, 255, 255), -1)

    cv2.imshow('Imagem Sobreposta com Pontos Marcados', overlay_image)
    print("Pressione 'q' para fechar a janela.")

    # Aguardar até que o usuário pressione 'q' para fechar a janela
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # Calcular distâncias entre os pontos marcados
    try:
        T1, D1, T2, D2 = mouse_params['marked_points']
    except ValueError:
        print("Marque exatamente 4 pontos (T1, D1, T2, D2) na imagem sobreposta.")
        return

    # Calcular a distância entre os pontos marcados (em pixels)
    distance_pixels = calculate_distance(T1[0], T1[1], D1[0], D1[1])  # Distância entre T1 e D1
    print(f"Distância euclidiana entre T1 e D1 em pixels: {distance_pixels:.2f}")

    # Calcular a velocidade do veículo
    try:
        velocidade_media_m_s, velocidade_media_km_h = calcular_velocidade_media(distance_pixels, tempo_gasto)
        print(f"Velocidade média do veículo: {velocidade_media_m_s:.2f} m/s ({velocidade_media_km_h:.2f} km/h)")
    except ValueError as e:
        print(f"Erro ao calcular velocidade média do veículo: {e}")

if __name__ == "__main__":
    main()
