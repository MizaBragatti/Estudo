import random
import time

def mostrar_lembrete(intervalo_segundos):
    frases = ler_frases()
    if not frases:
        print("Nenhuma frase cadastrada para exibir lembretes.")
        return

    print(f"\nIniciando lembretes a cada {intervalo_segundos} segundos. Pressione Ctrl+C para parar.")
    try:
        while True:
            frase_aleatoria = random.choice(frases)
            print(f"\n--- Lembrete: ---\n'{frase_aleatoria}'")
            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        print("\nLembretes parados.")