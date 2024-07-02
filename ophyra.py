import machine
import ujson
import urandom
import time

# Crear un arreglo de 1000 datos
data = [urandom.randint(0, 100) for _ in range(1000)]

# Convertir el arreglo a JSON
json_data = ujson.dumps(data)


# Función para dividir el JSON en fragmentos de tamaño manejable
def split_string(s, chunk_size):
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


# Calcular el tamaño del fragmento (65% de la capacidad de transmisión a 115200 baudios)
baud_rate = 115200
bytes_per_second = baud_rate // 8
chunk_size = int(bytes_per_second * 0.65)  # 65% de la capacidad de transmisión

# Dividir el JSON en fragmentos de tamaño manejable
chunks = split_string(json_data, chunk_size)

# Inicializar la conexión serial en UART2
uart = machine.UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

while True:
    # Enviar los fragmentos a través de la conexión serial
    for chunk in chunks:
        uart.write(chunk)
        time.sleep(0.1)  # Ajustar el tiempo de espera según sea necesario

    # Enviar un indicador de finalización
    uart.write(b'END')

    # Esperar la confirmación de recepción correcta
    start_time = time.ticks_ms()
    confirmed = False
    while time.ticks_diff(time.ticks_ms(), start_time) < 3000:
        if uart.any():
            response = uart.read()
            if response == b'OK':
                print("Recepción confirmada, cerrando conexión.")
                confirmed = True
                break

    if confirmed:
        break
    else:
        print("Tiempo de espera agotado, reiniciando envío.")
