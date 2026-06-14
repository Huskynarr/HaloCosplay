import cv2
import numpy as np
import time

# Kamera initialisieren (0 ist meistens die Standard-Pi-Kamera oder USB-Kamera)
cap = cv2.VideoCapture(0)

# Ueberpruefen, ob die Kamera erfolgreich gestartet wurde
if not cap.isOpened():
    print("Fehler: Kamera konnte nicht gefunden werden.")
    exit()

# Spartan HUD Farben (Hex/RGB) - BGR-Format fuer OpenCV
COLOR_HUD_BLUE = (255, 200, 0)
COLOR_WARNING_RED = (55, 63, 196) # Hex #c43f37 als BGR

def draw_hud(frame):
    height, width, _ = frame.shape
    
    # 1. Fadenkreuz (Crosshair) in die Mitte zeichnen
    center_x, center_y = int(width / 2), int(height / 2)
    cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), COLOR_HUD_BLUE, 2)
    cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), COLOR_HUD_BLUE, 2)
    cv2.circle(frame, (center_x, center_y), 40, COLOR_HUD_BLUE, 1)

    # 2. Status-Text simulieren (z.B. Schilde)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "SHIELDS: OPTIMAL", (20, 40), font, 0.7, COLOR_HUD_BLUE, 2, cv2.LINE_AA)
    
    # 3. Platzhalter fuer die Bluetooth-Telemetrie vom Arduino (Munition)
    cv2.putText(frame, "MA40 AMMO: 32", (width - 250, height - 40), font, 0.7, COLOR_WARNING_RED, 2, cv2.LINE_AA)
    
    return frame

def simulate_friend_foe(frame):
    # Basis-Simulation der Bilderkennung fuer Freund/Feind
    # (In einer erweiterten Version koennte hier ein Haar-Cascade oder YOLO-Modell zur Personenerkennung laufen)
    height, width, _ = frame.shape
    start_point = (int(width*0.25), int(height*0.25))
    end_point = (int(width*0.75), int(height*0.75))
    
    # Roter Rahmen simuliert ein erkanntes Ziel
    cv2.rectangle(frame, start_point, end_point, COLOR_WARNING_RED, 2)
    cv2.putText(frame, "TARGET DETECTED", (start_point[0], start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WARNING_RED, 1, cv2.LINE_AA)
    
    return frame

while True:
    # Frame fuer Frame einlesen
    ret, frame = cap.read()
    if not ret:
        print("Kamerafehler. Beende Stream.")
        break
    
    # Optionale Filter: z. B. Nachtsicht-Effekt (leicht gruener Tint)
    # frame[:, :, 0] = 0 # Blau-Kanal entfernen
    # frame[:, :, 2] = 0 # Rot-Kanal entfernen

    # HUD-Elemente ueber das Kamerabild legen
    frame = simulate_friend_foe(frame)
    frame = draw_hud(frame)
    
    # Das fertige Bild an das Display (Vufine/HDMI) ausgeben
    cv2.imshow('Mjolnir AR HUD', frame)
    
    # Skript beenden, wenn 'q' gedrueckt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Nach Beenden Ressourcen freigeben
cap.release()
cv2.destroyAllWindows()
