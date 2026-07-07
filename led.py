import time
import RPi.GPIO as GPIO

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Inicia o PWM no pino 18 com frequência inicial de 1 Hz
pwm_led = GPIO.PWM(LED_PIN, 1) 
pwm_led.start(50) # 50% de Duty Cycle

try:
    print("Testando frequências no LED...")
    
    # Frequência Baixa: O olho humano percebe o pisca-pisca
    print("Frequência: 2 Hz (Cintilação visível)")
    pwm_led.ChangeFrequency(2)
    time.sleep(4)
    
    # Frequência Média: Transição
    print("Frequência: 10 Hz")
    pwm_led.ChangeFrequency(10)
    time.sleep(4)
    
    # Frequência Alta: Efeito de esmaecimento (dimming) contínuo
    print("Frequência: 100 Hz (Fusão crítica de cintilação)")
    pwm_led.ChangeFrequency(100)
    
    # Variando o brilho a 100 Hz
    for brilho in range(0, 101, 20):
        print(f"Brilho do LED: {brilho}%")
        pwm_led.ChangeDutyCycle(brilho)
        time.sleep(1)

finally:
    pwm_led.stop()
    GPIO.cleanup()