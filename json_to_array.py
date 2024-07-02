import serial
import json

# Configuración del puerto serial
port = 'COM13'
baud_rate = 115200
ser = serial.Serial(port, baud_rate, timeout=1)

# Función para recibir datos en fragmentos y recomponer el JSON
def receive_json(ser):
    received_data = ""
    while True:
        chunk = ser.read(100)  # Leer en fragmentos pequeños
        if chunk:
            received_data += chunk.decode('utf-8')
            # Verificar si se recibe el indicador de finalización
            if 'END' in received_data:
                received_data = received_data.replace('END', '')
                break
    return received_data

while True:
    # Recibir los datos desde el puerto serial
    json_data = receive_json(ser)

    # Asegurarse de que los datos recibidos no están vacíos y son válidos
    if json_data:
        try:
            # Convertir el JSON a una lista de enteros
            data_array = json.loads(json_data)
            # Imprimir el arreglo recibido
            print("Arreglo recibido:", data_array)
            # Realizar una operación con el arreglo de enteros
            # Ejemplo: calcular la suma de los elementos del arreglo
            array_sum = sum(data_array)
            # Imprimir el resultado de la operación
            print("Suma de los elementos del arreglo:", array_sum)
            # Enviar confirmación de recepción correcta
            ser.write(b'OK')
            break
        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
    else:
        print("No se recibieron datos válidos.")

# Cerrar el puerto serial
ser.close()
