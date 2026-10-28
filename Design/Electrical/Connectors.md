# Steckerbelegung electrical-r1

Netze sind logische Kabelbaumbezeichnungen. Physische Gehaeuse/Kontakte,
Steckseite und Kodierung bleiben auszulegen; diese Nummern sind keine
universelle JST-, USB- oder RGB-Steckerbelegung. Gegenstecker passend
verdrahten und Durchgang vor dem Einschalten messen.

| Referenz | Anschluss | Netz | Bedeutung |
| --- | --- | --- | --- |
| J10 | 1 | C5_RAW | 5 V Komfort-Eingang; kodiert |
| J10 | 2 | C_GND | 5 V Komfort-Eingang; kodiert |
| J11 | 1 | C_GND | Helm links; 5-V-Noctua-PWM |
| J11 | 2 | C5_FAN | Helm links; 5-V-Noctua-PWM |
| J11 | 3 | NC, einzeln offen | Helm links; 5-V-Noctua-PWM |
| J11 | 4 | NC, einzeln offen | Helm links; 5-V-Noctua-PWM |
| J12 | 1 | C_GND | Helm rechts; 5-V-Noctua-PWM |
| J12 | 2 | C5_FAN | Helm rechts; 5-V-Noctua-PWM |
| J12 | 3 | NC, einzeln offen | Helm rechts; 5-V-Noctua-PWM |
| J12 | 4 | NC, einzeln offen | Helm rechts; 5-V-Noctua-PWM |
| J13 | 1 | C_GND | Torso links; 5-V-Noctua-PWM |
| J13 | 2 | C5_FAN | Torso links; 5-V-Noctua-PWM |
| J13 | 3 | NC, einzeln offen | Torso links; 5-V-Noctua-PWM |
| J13 | 4 | NC, einzeln offen | Torso links; 5-V-Noctua-PWM |
| J14 | 1 | C_GND | Torso rechts; 5-V-Noctua-PWM |
| J14 | 2 | C5_FAN | Torso rechts; 5-V-Noctua-PWM |
| J14 | 3 | NC, einzeln offen | Torso rechts; 5-V-Noctua-PWM |
| J14 | 4 | NC, einzeln offen | Torso rechts; 5-V-Noctua-PWM |
| J20 | VOUT | E15_RAW | SparkFun DEV-15801 / STUSB4500 |
| J20 | GND | E_GND | SparkFun DEV-15801 / STUSB4500 |
| J21 | 1 | MCU_READY | Temperaturkontaktkette; potentialfreie Oeffner |
| J21 | 2 | READY_AFTER_TH | Temperaturkontaktkette; potentialfreie Oeffner |
| J22 | 1 | E5_CTRL | MCU lokale Versorgung; 5 V IN -> eigene 3V3-Regelung |
| J22 | 2 | E_GND | MCU lokale Versorgung; 5 V IN -> eigene 3V3-Regelung |
| J30 | 1 | E_GND | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 2 | MCU_READY | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 3 | PWM_H_R | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 4 | PWM_H_G | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 5 | PWM_H_B | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 6 | PWM_N_R | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 7 | PWM_N_G | 3,3-V-MCU-Signale; nur Effektdomaene |
| J30 | 8 | PWM_N_B | 3,3-V-MCU-Signale; nur Effektdomaene |
| JHL | 1 | LED_H_R_OUT | RGB-Star; 6 getrennte Pads |
| JHL | 2 | LED_H_R_MID | RGB-Star; 6 getrennte Pads |
| JHL | 3 | LED_H_G_OUT | RGB-Star; 6 getrennte Pads |
| JHL | 4 | LED_H_G_MID | RGB-Star; 6 getrennte Pads |
| JHL | 5 | LED_H_B_OUT | RGB-Star; 6 getrennte Pads |
| JHL | 6 | LED_H_B_MID | RGB-Star; 6 getrennte Pads |
| JHR | 1 | LED_H_R_MID | RGB-Star; 6 getrennte Pads |
| JHR | 2 | LED_H_R_RET | RGB-Star; 6 getrennte Pads |
| JHR | 3 | LED_H_G_MID | RGB-Star; 6 getrennte Pads |
| JHR | 4 | LED_H_G_RET | RGB-Star; 6 getrennte Pads |
| JHR | 5 | LED_H_B_MID | RGB-Star; 6 getrennte Pads |
| JHR | 6 | LED_H_B_RET | RGB-Star; 6 getrennte Pads |
| JNL | 1 | LED_N_R_OUT | RGB-Star; 6 getrennte Pads |
| JNL | 2 | LED_N_R_MID | RGB-Star; 6 getrennte Pads |
| JNL | 3 | LED_N_G_OUT | RGB-Star; 6 getrennte Pads |
| JNL | 4 | LED_N_G_MID | RGB-Star; 6 getrennte Pads |
| JNL | 5 | LED_N_B_OUT | RGB-Star; 6 getrennte Pads |
| JNL | 6 | LED_N_B_MID | RGB-Star; 6 getrennte Pads |
| JNR | 1 | LED_N_R_MID | RGB-Star; 6 getrennte Pads |
| JNR | 2 | LED_N_R_RET | RGB-Star; 6 getrennte Pads |
| JNR | 3 | LED_N_G_MID | RGB-Star; 6 getrennte Pads |
| JNR | 4 | LED_N_G_RET | RGB-Star; 6 getrennte Pads |
| JNR | 5 | LED_N_B_MID | RGB-Star; 6 getrennte Pads |
| JNR | 6 | LED_N_B_RET | RGB-Star; 6 getrennte Pads |

Bei J11...J14 gilt die native Noctua-PWM-Belegung, bei den restlichen
J-Steckern die hier definierte Projektbelegung. Kein Powerbank-Ausgang
wird parallel mit einem anderen Ausgang verbunden.
