import machine
import time

storico = []  # Variabile globale per lo storico
run = False

def setGPSRun(state):
    global run
    run = state
    
def getGPS ():
    global storico
    return storico

def startGPS(storico_len=10):
    global storico  # Dichiarazione della variabile globale
    global run
    storico = []  # Svuota lo storico ad ogni chiamata

    uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

    while run:
        if uart.any():
            data = uart.read(1).decode('utf-8')
            storico.append(data)
            if len(storico) > storico_len:
                storico.pop(0)

            print(data, end='')  # Puoi rimuovere questa riga se preferisci non stampare ogni carattere

    return storico

# Utilizzo della funzione
storico_messaggi = leggi_gps(storico_len=20)
