import time
import RPi.GPIO as GPIO
import lgpio

# ==========================
# Definição dos pinos
# ==========================
LED_PIN = 17
BUZZER_PIN = 12
SERVO_PIN = 18

# ==========================
# Configuração do GPIO (LED e Buzzer)
# ==========================
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# PWM do LED
pwm_led = GPIO.PWM(LED_PIN, 100)
pwm_led.start(0)

# PWM do buzzer
pwm_buzzer = GPIO.PWM(BUZZER_PIN, 1000)
pwm_buzzer.start(0)

# ==========================
# Configuração do Servo (lgpio)
# ==========================
PWM_FREQ = 50

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, SERVO_PIN)

def set_angle(angle):
    angle = max(0, min(180, angle))
    duty = 2.5 + (angle / 180.0) * 10.0
    lgpio.tx_pwm(h, SERVO_PIN, PWM_FREQ, duty)

# ==========================
# Configuração do metrônomo
# ==========================
lado_esquerdo = True
DURACAO_BIPE = 0.05
INTERVALO = 1.0

print("Metrônomo iniciado. Pressione Ctrl+C para parar.")

try:
    while True:
        tempo_inicio = time.perf_counter()

        # Movimento do servo
        if lado_esquerdo:
            set_angle(0)
        else:
            set_angle(180)

        lado_esquerdo = not lado_esquerdo

        # Liga LED
        pwm_led.ChangeDutyCycle(100)

        # Liga buzzer
        pwm_buzzer.ChangeDutyCycle(50)

        # Tempo do clique
        time.sleep(DURACAO_BIPE)

        # Desliga LED e buzzer
        pwm_led.ChangeDutyCycle(0)
        pwm_buzzer.ChangeDutyCycle(0)

        # Compensação do tempo
        tempo_decorrido = time.perf_counter() - tempo_inicio
        tempo_restante = INTERVALO - tempo_decorrido

        if tempo_restante > 0:
            time.sleep(tempo_restante)
        else:
            print("Atenção: atraso na batida!")

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    # LED
    pwm_led.stop()

    # Buzzer
    pwm_buzzer.stop()

    # Servo
    lgpio.tx_pwm(h, SERVO_PIN, 0, 0)
    lgpio.gpiochip_close(h)

    # GPIO
    GPIO.cleanup()
