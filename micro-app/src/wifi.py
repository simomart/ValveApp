import network
import time

def set_ac(ssid, password):
    # Crea un oggetto WLAN e imposta la modalità AP
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    # Imposta le credenziali dell'AP con WPA2-PSK
    ap.config(essid=ssid, authmode=network.AUTH_WPA2_PSK, password=password)

    # Stampa il messaggio di conferma
    print("Access Point creato:")
    print("SSID: {}".format(ssid))
    print("Password: {}".format(password))
    print("Indirizzo IP: {}".format(ap.ifconfig()[0]))

    return ap

def set_client(ssid, password):
    # Crea un oggetto WLAN e imposta la modalità STATION (client)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    # Configura le credenziali del client WiFi
    sta_if.connect(ssid, password)

    # Attendi fino a quando la connessione è stabilita
    while not sta_if.isconnected():
        time.sleep(1)  # Pausa di 1 secondo durante l'attesa

    # Stampa il messaggio di conferma
    print("Connessione WiFi stabilita:")
    print("SSID: {}".format(ssid))
    print("Indirizzo IP: {}".format(sta_if.ifconfig()[0]))

    return sta_if