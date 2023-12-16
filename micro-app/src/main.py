import ubinascii
import machine
from machine import Pin, PWM, DAC
import gc
import _thread

import sys
sys.path.append('microWebSrv')
from microWebSrv.microWebSrv import MicroWebSrv
from wifi import set_ac, set_client

from analogRead import oscilloscope, getReadings, setOscilloscopeRun

from gpsRead import startGPS, getGPS, setGPSRun

machine.freq(240000000)


oscilloscope_running = False
gps_running = False

# Imposta il nome della rete e la password
ssid = "ESP-Test-Simone"
password = "password"
# ssid = "WebCube4-4A19"
# password = "T6GBY6Z3"


# Setta come access point
net=set_ac(ssid, password)
# net=set_client(ssid, password)

# Get microcontroller info
def info_endpoint(http_client, httpResponse):
    cpu_info = {
        "id": ubinascii.hexlify(machine.unique_id()).decode('utf-8'),
        "freq": machine.freq(),
    }
    
    # Informazioni sulla memoria
    memory_info = {
        "ram_free": gc.mem_free(),
        "ram_use": gc.mem_alloc(),
        "ram_total": gc.mem_alloc() + gc.mem_free(),
        "used_perc": gc.mem_alloc() / gc.mem_free() * 100,
    }
    
    # Informazioni di base sulla rete
    network_info = {
        "ssid": ssid,
        "password": password,
        "ip_address": net.ifconfig()[0],
    }

    # Unisci tutte le informazioni
    info = {
        "network": network_info,
        "cpu": cpu_info,
        "memory": memory_info,
    }

    httpResponse.WriteResponseJSONOk(info)

# Set PWM on PIN
def SetPWM (percent, pin, freq, httpResponse):
    try:
        # Convert percent to integer
        percent = int(percent)

        # Check if the percent value is within the valid range
        if percent < 0 or percent > 100:
            print("Percentage out of range (0-100)")
            return

        # Initialize PWM on the specified pin
        pwm_pin = PWM(Pin(int(pin)))
        pwm_pin.freq(freq)

        # Modify the duty_cycle_max accordingly
        duty_cycle_max = 1023

        # Calculate duty cycle based on the percentage
        duty_cycle = int((percent / 100) * duty_cycle_max)

        # Set PWM duty cycle
        pwm_pin.duty(duty_cycle)
        
        httpResponse.WriteResponseJSONOk({"Success":"True"})
    except Exception as ex:
        httpResponse.WriteResponseJSONOk({"Success":"False", "Message": str(ex)})

# Set analog
def SetAnalog(percent, pin, httpResponse):
    try:
        # Converti la percentuale in intero
        percent = int(percent)

        # Controlla se il valore percentuale è nel range valido (0-100)
        if percent < 0 or percent > 100:
            print("Percentage out of range (0-100)")
            return

        # Verifica che il pin sia uno dei pin DAC validi (25 o 26)
        if pin not in [25, 26]:
            httpResponse.WriteResponseJSONOk({"Success":"False", "Message": "Invalid DAC pin"})
            return

        # Inizializza DAC sul pin specificato
        dac = DAC(Pin(pin))

        # Calcola il valore per DAC (0-255) in base alla percentuale
        dac_value = int((percent / 100) * 255)

        # Imposta il valore DAC
        dac.write(dac_value)

        httpResponse.WriteResponseJSONOk({"Success":"True"})
    except Exception as ex:
        httpResponse.WriteResponseJSONOk({"Success":"False", "Message": str(ex)})

@MicroWebSrv.route('/info')
def handlerFuncGet(httpClient, httpResponse):
    info_endpoint(httpClient, httpResponse)
    
@MicroWebSrv.route('/startGPS')
def handlerFuncGet(httpClient, httpResponse):
    setGPSRun(True)
    _thread.start_new_thread(startGPS, ())
    httpResponse.WriteResponseJSONOk({"Success":"True"})

@MicroWebSrv.route('/stopGPS')
def handlerFuncGet(httpClient, httpResponse):
    setGPSRun(False)
    httpResponse.WriteResponseJSONOk({"Success":"True"})

@MicroWebSrv.route('/getGPS')
def handlerFuncGet(httpClient, httpResponse):
    httpResponse.WriteResponseJSONOk({"Success":"True", "Readings": getGPS()})
    
@MicroWebSrv.route('/startOscilloscope/<microseconds>/pin/<pin>/readings/<readings>')
def handlerFuncGet(httpClient, httpResponse, routeArgs):
    setOscilloscopeRun(True)
    #_thread.start_new_thread(oscilloscope, (10000, 100, 34))
    _thread.start_new_thread(oscilloscope, (routeArgs["readings"], routeArgs["microseconds"], routeArgs["pin"]))
    httpResponse.WriteResponseJSONOk({"Success":"True"})

@MicroWebSrv.route('/stopOscilloscope')
def handlerFuncGet(httpClient, httpResponse):
    setOscilloscopeRun(False)
    httpResponse.WriteResponseJSONOk({"Success":"True"})

@MicroWebSrv.route('/getOscilloscopeData')
def handlerFuncGet(httpClient, httpResponse):
    httpResponse.WriteResponseJSONOk({"Success":"True", "Readings": getReadings()})
    
@MicroWebSrv.route('/setpwm/<percent>/pin/<pin>/freq/<freq>')
def handlerFuncGet(httpClient, httpResponse, routeArgs):
    SetPWM(routeArgs["percent"], routeArgs["pin"], routeArgs["freq"], httpResponse)
    
@MicroWebSrv.route('/setdac/<percent>/pin/<pin>')
def handlerFuncGet(httpClient, httpResponse, routeArgs):
    SetAnalog(routeArgs["percent"], routeArgs["pin"], httpResponse)
    
# @MicroWebSrv.route('/post-test', 'POST')
# def handlerFuncPost(httpClient, httpResponse) :
#   print("In POST-TEST HTTP")
# @MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
# @MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
# @MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
  
# Avvia il server
srv = MicroWebSrv(webPath='html/')
srv.MaxWebSocketRecvLen     = 256
srv.Start(threaded=False)