import cv2

def capture_video(input_file, output_file, frame_extraction_interval):
    
    # Captura de vídeo
    cap = cv2.VideoCapture(input_file)
    
    # Verifica se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    # Propriedades do vídeo
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Configura o escritor de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if ret:
            # Escreve o frame no arquivo de saída
            out.write(frame)
            
            # Exibe o frame
            cv2.imshow('Frame', frame)
            
            frame_count += 1
            
            # Extrai um frame a cada intervalo especificado
            if frame_count % frame_extraction_interval == 0:
                cv2.imwrite(f"frame_{frame_count}.jpg", frame)
            
            # Fecha a janela ao pressionar 'q'
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    
    # Libera os recursos
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Exemplo de uso
input_file = 'Midia/RC.mp4'
output_file = 'Midia/Frames.avi'
frame_extraction_interval = 1000  # Extrai um frame a cada 100 frames

capture_video(input_file, output_file, frame_extraction_interval)
