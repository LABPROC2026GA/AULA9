import time
import RPi.GPIO as GPIO

SERVO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Servomotores operam estritamente a 50Hz
pwm_servo = GPIO.PWM(SERVO_PIN, 50)
pwm_servo.start(0)

try:
    print("Testando posições do Servomotor...")
    
    print("Posição: 0 graus")
    pwm_servo.ChangeDutyCycle(2.5) # Pulso de 0.5ms
    time.sleep(2)
    
    print("Posição: 90 graus (Centro)")
    pwm_servo.ChangeDutyCycle(7.5) # Pulso de 1.5ms
    time.sleep(2)
    
    print("Posição: 180 graus")
    pwm_servo.ChangeDutyCycle(12.5) # Pulso de 2.5ms
    time.sleep(2)

finally:
    pwm_servo.stop()
    GPIO.cleanup()