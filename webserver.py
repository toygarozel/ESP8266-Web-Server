import machine

led = machine.Pin(2, machine.Pin.OUT)
led.on()

def led_toggle(pin):
    if pin.value() == 1:
        pin.off()
    elif pin.value() == 0:
        pin.on()
    else:
        pass
    
import network
import wifi_credentials

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    sta.active(True)
    sta.connect(wifi_credentials.ssid, wifi_credentials.password)
    while not sta.isconnected():
        pass

print("IP addresses")
print(sta.ifconfig())


import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('',80))
server_socket.listen(5)
                   
def request_handler(req):
    request = req.split()[1]
    if (request == "/?LED_BUILTIN=0"):
        led.on()
    elif (request == "/?LED_BUILTIN=1"):
        led.off()
    elif (request == "/?LED_BUILTIN=2"):
        led_toggle(led)
    else:
        pass

def create_http_response(value):
    f = open("home.html", "r")
    html_page = "HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n" + f.read()
    f.close()
    if value == 0:
        status = "ON"
    else:
        status = "OFF"
    led_status = "<p style=\"text-align: center;font-size: 35px\">LED STATUS = <span style=\"color: #56FFF2\"> %s </span></p>" % status
    response = html_page + led_status
    return response

while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024)
    request_handler(str(request))
    response = create_http_response(led.value())
    conn.sendall(response)
    
    conn.close()