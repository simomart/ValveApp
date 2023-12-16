import machine
import time
import utime

# storico = []  # Variabile globale per lo storico
rilevazione = []
run = False

def format_time(timestamp, offset_hours):
    # Converti timestamp in formato leggibile con offset orario
    year = int(timestamp[4:6]) + 2000
    month = int(timestamp[2:4])
    day = int(timestamp[0:2])
    hour = int(timestamp[6:8])
    minute = int(timestamp[8:10])
    second = int(timestamp[10:12])

    # Aggiungi l'offset orario
    hour = (hour + offset_hours) % 24

    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
    return formatted_time


def setGPSRun(state):
    global run
    run = state
    
def getGPS():
    # global storico
    global rilevazione
    return rilevazione

def startGPS():
    global run
    global rilevazione
    
    datetime = ""
    lat = 0
    lon = 0
    alt = 0
    speed = 0
    satellite = 0
    
    storico = []

    uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

    while run:
        try:
            if uart.any():
                riga_completa = uart.readline().decode('ascii')

                # Verifica se la riga è completa e inizia con "$GPRMC" o "$GPGGA"
                if riga_completa.startswith("$GPRMC"):
                    # Suddivide i campi del messaggio NMEA
                    fields = riga_completa.split(',')

                    # Verifica la validità del messaggio
                    # if len(fields) >= 12 and fields[2] == 'A':
                    # Estrai i dati necessari
                    lat = float(fields[3]) / 100 if fields[3] else "***"
                    lon = float(fields[5]) / 100 if fields[5] else "***"
                    speed = float(fields[7]) if fields[7] else "***"

                    date_str = fields[9] if fields[9] else "***"
                    time_str = fields[1] if fields[1] else "***"
                    
                    satellite = int(fields[8]) if fields[8] else "***"


                    # Converti la data e l'ora in un formato più leggibile
                    timestamp = date_str + time_str
                    datetime = format_time(timestamp, offset_hours=1)
                    
                    # Creare l'elemento nel formato richiesto e aggiungere allo storico
                    rilevazione = [datetime, lat, lon, alt, speed, satellite]
                    print(rilevazione)

                elif riga_completa.startswith("$GPGGA"):
                    # Suddivide i campi del messaggio NMEA
                    fields = riga_completa.split(',')

                    alt = float(fields[9]) if fields[9] else "***"

                    # date_str = fields[1] if fields[1] else "***"
                    # time_str = fields[0] if fields[0] else "***"

                    # Converti la data e l'ora in un formato più leggibile
                    # timestamp = date_str + time_str
                    # datetime = format_time(timestamp)

                    # Creare l'elemento nel formato richiesto e aggiungere allo storico
                    rilevazione = [datetime, lat, lon, alt, speed, satellite]
                    print(rilevazione)

        except Exception as e:
            print(e)
        time.sleep(0.01)  # Aggiungi una breve pausa per evitare problemi di buffering
