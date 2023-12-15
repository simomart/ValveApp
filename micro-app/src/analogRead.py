import machine
import time

readings = [(0,0)]
run = False

def setOscilloscopeRun(state):
    global run
    run = state

def getReadings():
    return readings

def oscilloscope(max_saved_values = 1000, us_interval = 100, pin = 34):
    global readings
    global run
    
     # Configura il pin analogico
    adc_pin = machine.Pin(pin)
    adc = machine.ADC(adc_pin)

    # Configura l'ADC
    adc.width(machine.ADC.WIDTH_12BIT)
    adc.atten(machine.ADC.ATTN_11DB)

    # Inizializza un array circolare per salvare le letture
    max_readings = max_saved_values
    readings = [(0, 0)] * max_readings
    current_index = 0

    # Imposta l'intervallo di tempo tra le letture in microsecondi
    reading_interval_us = us_interval  # Modifica questo valore per cambiare l'intervallo

    # Ottieni il tempo iniziale
    last_reading_time = time.ticks_us()

    while run:
        current_time = time.ticks_us()
        # Controlla se è il momento di fare una nuova lettura
        if time.ticks_diff(current_time, last_reading_time) >= reading_interval_us:
            val = adc.read()
            timestamp = current_time
            readings[current_index] = (val, timestamp)
            current_index = (current_index + 1) % max_readings
            last_reading_time = current_time
