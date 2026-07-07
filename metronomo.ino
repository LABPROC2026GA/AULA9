import RPi.GPIO as GPIO
import time
import threading

# 1. DEFINIÇÃO DE PINOS (Padrão BCM)
PIN_LED = 18
PIN_SERVO = 12
PIN_BUZZER = 23
PIN_BTN_UP = 24
PIN_BTN_DOWN = 25

# Variáveis globais de controle
bpm = 60 # 60 Batidas por minuto = 1 Hz
executando = True
posicao_servo = False # Alternador de posição do braço do servo

# 2. CONFIGURAÇÃO DA GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuração de Saídas
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_BUZZER, GPIO.OUT)

# Configuração de Entradas (Botões com Pull-Up interno)
GPIO.setup(PIN_BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Inicialização do PWM
# LED: 1kHz para estabilidade visual
pwm_led = GPIO.PWM(PIN_LED, 1000) 
pwm_led.start(0)

# SERVO: 50Hz (Período de 20ms cravado)
pwm_servo = GPIO.PWM(PIN_SERVO, 50)
pwm_servo.start(0)

# 3. FUNÇÕES DE CONTROLE ISOLADO
def controle_led(duty_cycle):
    """Controla o brilho do LED (0 a 100%)"""
    pwm_led.ChangeDutyCycle(duty_cycle)

def controle_servo(largura_pulso_ms):
    """
    1.0ms -> ~5% (Posição 1)
    1.5ms -> ~7.5% (Centro)
    2.0ms -> ~10% (Posição 2)
    """
    duty_cycle = (largura_pulso_ms / 20.0) * 100
    pwm_servo.ChangeDutyCycle(duty_cycle)

def bip_buzzer(duracao=0.05):
    """Ativa o buzzer por um curto período"""
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    time.sleep(duracao)
    GPIO.output(PIN_BUZZER, GPIO.LOW)

# 4. RESOLUÇÃO DO DESAFIO (INTERRUPÇÕES E BOUNCING)
def callback_btn_up(channel):
    global bpm
    bpm += 5
    print(f"BPM Aumentado: {bpm}")

def callback_btn_down(channel):
    global bpm
    if bpm > 10: # Evita BPM negativo ou muito lento
        bpm -= 5
    print(f"BPM Reduzido: {bpm}")

# Event Detect com Debouncing de 200ms nativo da biblioteca
GPIO.add_event_detect(PIN_BTN_UP, GPIO.FALLING, callback=callback_btn_up, bouncetime=200)
GPIO.add_event_detect(PIN_BTN_DOWN, GPIO.FALLING, callback=callback_btn_down, bouncetime=200)

# 5. THREAD PRINCIPAL: INTEGRAÇÃO E TEMPORIZAÇÃO (DRIFT)
def loop_metronomo():
    global executando, posicao_servo
    
    print("Iniciando Metrônomo... Pressione CTRL+C para sair.")
    
    try:
        while executando:
            # Captura o tempo no início do ciclo
            tempo_inicio = time.time()
            
            # Calcula o intervalo alvo em segundos com base no BPM atual
            intervalo_alvo = 60.0 / bpm
            
            # --- EXECUÇÃO DOS ATUADORES ---
            # 1. Move o Servomotor (alternando entre 1.0ms e 2.0ms)
            if posicao_servo:
                controle_servo(2.0)
            else:
                controle_servo(1.0)
            posicao_servo = not posicao_servo
            
            # 2. Acende o LED no pico (100%) e aciona o Buzzer
            controle_led(100)
            bip_buzzer(0.05)
            controle_led(0) # Apaga o LED
            
            # --- COMPENSAÇÃO DE DRIFT (Jitter do SO) ---
            # Calcula quanto tempo o laço demorou para rodar os atuadores
            tempo_execucao_do_laco = time.time() - tempo_inicio
            
            # O tempo de espera é o intervalo alvo menos o tempo que já passou
            drift_time = tempo_execucao_do_laco
            tempo_espera = intervalo_alvo - drift_time
            
            # Proteção: só dorme se houver tempo restante (evita erro caso o SO trave a thread)
            if tempo_espera > 0:
                time.sleep(tempo_espera)
                
    except KeyboardInterrupt:
        print("\nEncerrando execução...")
    finally:
        # Rotina de depuração/limpeza
        pwm_led.stop()
        pwm_servo.stop()
        GPIO.cleanup()
        print("GPIO limpa com sucesso. Fim do programa.")

# Inicia a thread principal
if __name__ == '__main__':
    loop_metronomo()