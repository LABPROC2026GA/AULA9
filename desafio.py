import time
from gpiozero import Button, PWMLED, TonalBuzzer, Servo
from gpiozero.tones import Tone

# ==========================
# Configuração dos pinos
# ==========================
BTN_UP_PIN = 20
BTN_DOWN_PIN = 21

BUZZER_PIN = 12
SERVO_PIN = 18
LED_PIN = 17

btn_up = Button(BTN_UP_PIN, pull_up=True)
btn_down = Button(BTN_DOWN_PIN, pull_up=True)

buzzer = TonalBuzzer(BUZZER_PIN)
servo = Servo(SERVO_PIN)
led = PWMLED(LED_PIN)

# ==========================
# Configuração do metrônomo
# ==========================
bpm = 60
MIN_BPM = 30
MAX_BPM = 240

DURACAO_BATIDA = 0.05

posicao_servo = -1


def aumentar_bpm():
    global bpm

    if bpm < MAX_BPM:
        bpm += 5
        print(f"BPM: {bpm}")


def diminuir_bpm():
    global bpm

    if bpm > MIN_BPM:
        bpm -= 2
        print(f"BPM: {bpm}")


# Botões
btn_up.when_pressed = aumentar_bpm
btn_down.when_pressed = diminuir_bpm


print(f"Metrônomo iniciado em {bpm} BPM")
print("Botão GPIO 2 aumenta | GPIO 3 diminui")


try:
    while True:

        inicio = time.perf_counter()

        # Tempo entre batidas
        intervalo = 60 / bpm

        # Movimento do pêndulo
        servo.value = posicao_servo

        # Pulso visual e sonoro
        led.value = 1
        buzzer.play(Tone(440))

        time.sleep(DURACAO_BATIDA)

        buzzer.stop()
        led.value = 0


        # Alterna servo
        if posicao_servo == -1:
            posicao_servo = 1
        else:
            posicao_servo = -1


        # Compensa tempo gasto
        decorrido = time.perf_counter() - inicio
        restante = intervalo - decorrido

        if restante > 0:
            time.sleep(restante)


except KeyboardInterrupt:
    print("\nEncerrando metrônomo...")


finally:
    buzzer.stop()
    servo.close()
    led.close()
    btn_up.close()
    btn_down.close()
