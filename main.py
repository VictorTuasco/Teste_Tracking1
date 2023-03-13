import cv2
import mediapipe as mp
import datetime

camera = cv2.VideoCapture(0)

solucao_reconhecimento = mp.solutions.pose
reconhecedor = solucao_reconhecimento.Pose()
desenho = mp.solutions.drawing_utils

contador = 0
pose_detectada = False  # variável para controlar se uma pose está detectada

if camera.isOpened():
    validacao, frame = camera.read()
    fps = 15 # definir o FPS do vídeo para 30
    while validacao:
        validacao, frame = camera.read()

        # reconhecer pose
        lista_pose = reconhecedor.process(frame)
        if lista_pose.pose_landmarks is not None:
            # desenho.draw_landmarks(frame, lista_pose.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS) # remover esta linha para desativar o desenho
            if not pose_detectada:
                # Salvar o vídeo
                contador += 1
                nome_arquivo = datetime.datetime.now().strftime("pose_%d-%m-%Y_%H-%M-%S.mp4")
                writer = cv2.VideoWriter(nome_arquivo, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame.shape[1], frame.shape[0]))
                pose_detectada = True
                tempo_inicial = datetime.datetime.now()

            # Escrever o frame no vídeo
            writer.write(frame)

            # Verificar se o vídeo tem mais de 5 segundos
            tempo_atual = datetime.datetime.now()
            if (tempo_atual - tempo_inicial).total_seconds() >= 5:
                writer.release()
                pose_detectada = False

        else:
            pose_detectada = False

        cv2.imshow("pose", frame)
        key = cv2.waitKey(5)
        if key == 27:  # ESC
            break

camera.release()
cv2.destroyAllWindows()
