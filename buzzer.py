import time
import RPi.GPIO as GPIO

BUZZER_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Inicia com uma frequência de 440 Hz (Nota Lá)
pwm_buzzer = GPIO.PWM(BUZZER_PIN, 440)

try:
    print("Testando sons no Buzzer...")
    pwm_buzzer.start(50) # 50% de volume/Duty Cycle
    time.sleep(1)
    
    print("Mudando para 880 Hz (Tom mais agudo)")
    pwm_buzzer.ChangeFrequency(880)
    time.sleep(1)
    
    print("Desligando o som...")
    pwm_buzzer.ChangeDutyCycle(0) # Silêncio

finally:
    pwm_buzzer.stop()
    GPIO.cleanup()