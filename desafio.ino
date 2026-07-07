import RPi.GPIO as GPIO
import time

# 1. DEFINIÇÃO DOS PINOS (Norma BCM)
PIN_BOTAO_AUMENTAR = 24
PIN_BOTAO_DIMINUIR = 25

# Variável global para armazenar a frequência
# 60 BPM (Batimentos Por Minuto) equivale a 1 Hz
bpm = 60 

# 2. CONFIGURAÇÃO DA GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuração dos pinos de entrada com resistências de Pull-Up internas ativadas.
# Isto significa que o pino lerá nível lógico ALTO (HIGH) por predefinição.
# Quando o botão for premido e ligar o pino ao GND (Terra), a leitura passará a BAIXO (LOW).
GPIO.setup(PIN_BOTAO_AUMENTAR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BOTAO_DIMINUIR, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 3. ROTINAS DE INTERRUPÇÃO (CALLBACKS)
def aumentar_frequencia(canal):
    global bpm
    bpm += 5
    print(f"[+] Botão AUMENTAR premido. Nova frequência: {bpm} BPM")

def diminuir_frequencia(canal):
    global bpm
    # Impede que o BPM desça abaixo de zero ou assuma valores ilógicos
    if bpm > 10:
        bpm -= 5
        print(f"[-] Botão DIMINUIR premido. Nova frequência: {bpm} BPM")
    else:
        print(f"[!] Frequência mínima atingida: {bpm} BPM")

# 4. CONFIGURAÇÃO DOS EVENTOS COM DEBOUNCING
# Deteta a transição de nível ALTO para BAIXO (GPIO.FALLING), que ocorre no momento exato
# em que o botão é premido.
# O parâmetro 'bouncetime=200' faz com que o processador ignore oscilações ruidosas 
# (contactos falsos) durante 200 milissegundos após o primeiro sinal.
GPIO.add_event_detect(PIN_BOTAO_AUMENTAR, GPIO.FALLING, callback=aumentar_frequencia, bouncetime=200)
GPIO.add_event_detect(PIN_BOTAO_DIMINUIR, GPIO.FALLING, callback=diminuir_frequencia, bouncetime=200)

# 5. LOOP PRINCIPAL DE TESTE
def testar_botoes():
    print("--- Teste do Desafio: Controlo de BPM ---")
    print(f"Frequência inicial: {bpm} BPM")
    print("Pressione os botões físicos para alterar os valores.")
    print("Prima CTRL+C para terminar o programa.\n")
    
    try:
        # Um loop infinito leve, apenas para manter o programa a correr
        # enquanto as rotinas de interrupção operam em segundo plano
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado pelo utilizador.")
    finally:
        GPIO.cleanup()
        print("Pinos GPIO libertados de forma segura.")

# Ponto de entrada do ficheiro
if __name__ == '__main__':
    testar_botoes()