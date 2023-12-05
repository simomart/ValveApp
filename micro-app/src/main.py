import ubinascii
import machine
from machine import Pin, PWM
import gc

import sys
sys.path.append('microWebSrv')
from microWebSrv.microWebSrv import MicroWebSrv
from wifi import set_ac, set_client

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
def SetPWM (percent, pin, httpResponse):
    try:
        # Convert percent to integer
        percent = int(percent)

        # Check if the percent value is within the valid range
        if percent < 0 or percent > 100:
            print("Percentage out of range (0-100)")
            return

        # Initialize PWM on the specified pin
        pwm_pin = PWM(Pin(int(pin)))
        pwm_pin.freq(1000)

        # Modify the duty_cycle_max accordingly
        duty_cycle_max = 1023

        # Calculate duty cycle based on the percentage
        duty_cycle = int((percent / 100) * duty_cycle_max)

        # Set PWM duty cycle
        pwm_pin.duty(duty_cycle)
        
        httpResponse.WriteResponseJSONOk({"Success":"True"})
    except Exception as ex:
        httpResponse.WriteResponseJSONOk({"Success":"False", "Message": ex})

@MicroWebSrv.route('/info')
def handlerFuncGet(httpClient, httpResponse):
    info_endpoint(httpClient, httpResponse)
    
@MicroWebSrv.route('/setpwm/<percent>/pin/<pin>')
def handlerFuncGet(httpClient, httpResponse, routeArgs):
    SetPWM(routeArgs["percent"], routeArgs["pin"], httpResponse)
    
# @MicroWebSrv.route('/post-test', 'POST')
# def handlerFuncPost(httpClient, httpResponse) :
#   print("In POST-TEST HTTP")
# @MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
# @MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
# @MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
  
# Avvia il server
srv = MicroWebSrv(webPath='html/')
srv.MaxWebSocketRecvLen     = 256
srv.Start(threaded=True)