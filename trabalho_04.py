import cv2
import mediapipe as mp
import keyboard
import math
import time

def calcular_angulo(x1, y1, x2, y2):
    # Cálculo do ângulo entre dois pontos
    delta_x = x2 - x1
    delta_y = y2 - y1

    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    angle_degrees = angle_degrees % 360

    return angle_degrees


# Inicialização da webcam e detecção de mãos
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils

while True:

    ret, frame = webcam.read()
    frame_height, frame_width, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        if len(hands) == 2:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = hand.landmark

                # Captura das coordenadas de pontos específicos da mão
                # Cada ponto representa uma articulação
                for idx, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    if idx == 6:  # dedo indicador
                        cv2.circle(img=frame, center=(x, y), radius=6, color=(255, 255, 255), thickness=4)
                        if hand == hands[0]:
                            x1, y1 = x, y
                        else:
                            x3, y3 = x, y

                    if idx == 4:  # polegar
                        cv2.circle(img=frame, center=(x, y), radius=6, color=(255, 255, 255), thickness=4)
                        if hand == hands[0]:
                            x2, y2 = x, y
                        else:
                            x4, y4 = x, y

                    if idx == 13:  # Dedo indicador
                        cv2.circle(img=frame, center=(x, y), radius=6, color=(0, 0, 0), thickness=4)
                        if hand == hands[0]:
                            x5, y5 = x, y
                        else:
                            x6, y6 = x, y

                    if idx == 8:  # Dedo indicador ponta
                        cv2.circle(img=frame, center=(x, y), radius=6, color=(255, 0, 255), thickness=4)
                        if hand == hands[0]:
                            x7, y7 = x, y
                        else:
                            x9, y9 = x, y

                    if idx == 10:  # Dedo indicador
                        cv2.circle(img=frame, center=(x, y), radius=6, color=(255, 0, 255), thickness=4)
                        if hand == hands[0]:
                            x8, y8 = x, y
                        else:
                            x10, y10 = x, y

            # Cálculo de distâncias entre pontos e detecção de gestos de mão
            # Ativação de teclas de acordo com gestos específicos

            linha_freio = cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            linha_acelerador = cv2.line(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
            linha_virar = cv2.line(frame, (x5, y5), (x6, y6), (0, 0, 0), 2) 
            linha_re = cv2.line(frame, (x7, y7), (x8, y8), (0, 0, 255), 2)
            linha_nitro = cv2.line(frame, (x9, y9), (x10, y10), (255, 255, 0), 2)


            dist_freio = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5)
            dist_acelerador = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** (0.5)
            dist_re = ((x8 - x7) ** 2 + (y8 - y7) ** 2) ** (0.5)
            dist_nitro = ((x10 - x9) ** 2 + (y10 - y9) ** 2) ** (0.5)

            angulo_linha_virar = calcular_angulo(x5, y5, x6, y6)

            # print("dist_re= ", dist_re)
            # print("dist_acelerador= ", dist_acelerador)
            # print("dist_freio= ", dist_freio)
            # print("angulo_linha_virar= ", angulo_linha_virar) 

            if(dist_re >= 55 and dist_re >= dist_acelerador):
                # print("dando ré")
                keyboard.press('s')
            else:
                keyboard.release('s')
                

            if(dist_freio >= 55 and dist_freio >= dist_re):
                # print("freiando")
                keyboard.press('space')
            else:
                keyboard.release('space')


            if(dist_acelerador >= 55 and dist_acelerador >= dist_re):
                # print("acelerando!")
                keyboard.press('w')
            else:
                keyboard.release('w')
            

            if(dist_nitro >= 55):
                # print("nitrooo!")
                keyboard.press('ctrl')
            else:
                keyboard.release('ctrl')


            if(angulo_linha_virar >= 215):
                print("0.3 esquerda")
                keyboard.press('a')
                time.sleep(0.3)
                keyboard.release('a')
            elif(angulo_linha_virar >= 200):
                print("0.2 esquerda")
                keyboard.press('a')
                time.sleep(0.2)
                keyboard.release('a')
            elif(angulo_linha_virar >= 190):
                print("0.1 esquerda")
                keyboard.press('a')
                time.sleep(0.1)
                keyboard.release('a')
            
            elif(angulo_linha_virar <= 145):
                print("0.3 direita")
                keyboard.press('d')
                time.sleep(0.3)
                keyboard.release('d')
            elif(angulo_linha_virar <= 160):
                print("0.2 direita")
                keyboard.press('d')
                time.sleep(0.2)
                keyboard.release('d')
            elif(angulo_linha_virar <= 170):
                print("0.1 direita")
                keyboard.press('d')
                time.sleep(0.1)
                keyboard.release('d')
            

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
            

    cv2.imshow("webcam", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
