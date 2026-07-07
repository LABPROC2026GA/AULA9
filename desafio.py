import time
from gpiozero import Button, PWMLED, TonalBuzzer, Servo
from gpiozero.tones import Tone

# Configuração de Pinos
btn_up = Button(2)     # Botão para aumentar BPM no GPIO 2
btn_down = Button(3)   # Botão para diminuir BPM no GPIO 3
buzzer = TonalBuzzer(17)
servo = Servo(18)      # Recomenda-se rodar o daemon pigpiod para evitar jitter
led = PWMLED(27)

# Variáveis globais do Metrônomo
bpm = 60
min_bpm, max_bpm = 30, 240
rodando = True

def aumentar_bpm():
    global bpm
    if bpm < max_bpm:
        bpm += 5
        print(f"BPM: {bpm}")

def diminuir_bpm():
    global bpm
    if bpm > min_bpm:
        bpm -= 5
        print(f"BPM: {bpm}")

# Vinculando interrupções aos botões físicos
btn_up.when_pressed = aumentar_bpm
btn_down.when_pressed = diminuir_bpm

posicao_servo = -1.0 # -1.0 (min) a 1.0 (max)

print(f"Metrônomo iniciado a {bpm} BPM. Use os botões para alterar.")

try:
    while True:
        # Calcula o intervalo em segundos baseado no BPM atual
        intervalo = 60.0 / bpm
        
        # Ação do Metrônomo
        servo.value = posicao_servo
        led.value = 1.0
        buzzer.play(Tone("A4")) # Toca um som
        time.sleep(0.05)        # Duração curta do "bip" visual e sonoro
        buzzer.stop()
        led.value = 0.0
        
        # Inverte a posição do servo para a próxima batida
        posicao_servo = 1.0 if posicao_servo == -1.0 else -1.0
        
        # Espera o resto do tempo da batida
        # Subtrai o 0.05s já consumido pelo bipe
        time.sleep(intervalo - 0.05)

except KeyboardInterrupt:
    print("Metrônomo encerrado.")
    buzzer.stop()
    servo.detach()