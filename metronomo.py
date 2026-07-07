import time
import RPi.GPIO as GPIO

# Definição dos Pinos
LED_PIN = 18
SERVO_PIN = 23
BUZZER_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_PIN, SERVO_PIN, BUZZER_PIN], GPIO.OUT)

# Inicialização dos PWMs
pwm_led = GPIO.PWM(LED_PIN, 100)      # 100Hz para controle de brilho limpo
pwm_servo = GPIO.PWM(SERVO_PIN, 50)    # 50Hz obrigatório para o Servo
pwm_buzzer = GPIO.PWM(BUZZER_PIN, 1000) # 1000Hz para um bipe estalado

pwm_led.start(0)
pwm_servo.start(2.5) # Começa em 0 graus
pwm_buzzer.start(0)  # Começa em silêncio

# Estado do movimento do metrônomo
lado_esquerdo = True
DURACAO_BIPE = 0.05 # 50 milissegundos para o clique não ficar irritante

print("Metrônomo integrado iniciado (Intervalo: 1 segundo). Pressione Ctrl+C para parar.")

try:
    while True:
        tempo_inicio = time.perf_counter()
        
        # 1. Atua o Servo (Alterna o lado)
        if lado_esquerdo:
            pwm_servo.ChangeDutyCycle(2.5)  # 0 graus
        else:
            pwm_servo.ChangeDutyCycle(12.5) # 180 graus
        lado_esquerdo = not lado_esquerdo
        
        # 2. Atua o LED e o Buzzer (Dispara o sinal de batida)
        pwm_led.ChangeDutyCycle(100)    # LED no brilho máximo
        pwm_buzzer.ChangeDutyCycle(50)  # Ativa o som do buzzer
        
        time.sleep(DURACAO_BIPE)        # Aguarda a duração do bipe
        
        # 3. Desliga o sinal de batida (Mantém o servo na posição)
        pwm_led.ChangeDutyCycle(0)
        pwm_buzzer.ChangeDutyCycle(0)
        
        # 4. Cálculo de Compensação de Tempo
        tempo_decorrido = time.perf_counter() - tempo_inicio
        tempo_restante = 1.0 - tempo_decorrido
        
        if tempo_restante > 0:
            time.sleep(tempo_restante)
        else:
            print("Alerta: Sobrecarga no processamento, atraso na batida!")

except KeyboardInterrupt:
    print("\nFinalizando o metrônomo com segurança...")
finally:
    pwm_led.stop()
    pwm_servo.stop()
    pwm_buzzer.stop()
    GPIO.cleanup()