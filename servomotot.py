import lgpio
import time

SERVO_PIN = 18
PWM_FREQ = 50

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, SERVO_PIN)

def set_angle(angle):
    # Limita entre 0 e 180 graus
    angle = max(0, min(180, angle))

    # Converte para duty cycle (2.5% a 12.5%)
    duty = 2.5 + (angle / 180.0) * 10.0

    lgpio.tx_pwm(h, SERVO_PIN, PWM_FREQ, duty)

try:
    print("0°")
    set_angle(0)
    time.sleep(2)

    print("90°")
    set_angle(90)
    time.sleep(2)

    print("180°")
    set_angle(180)
    time.sleep(2)

finally:
    # Desliga o PWM
    lgpio.tx_pwm(h, SERVO_PIN, 0, 0)
    lgpio.gpiochip_close(h)
