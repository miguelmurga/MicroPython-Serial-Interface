import serial
import json

# Serial port configuration
port = 'COM13'
baud_rate = 115200
ser = serial.Serial(port, baud_rate, timeout=1)

# Function to receive data in chunks and reassemble JSON
def receive_json(ser):
    received_data = ""
    while True:
        chunk = ser.read(100)  # Read in small chunks
        if chunk:
            received_data += chunk.decode('utf-8')
            # Check for end marker
            if 'END' in received_data:
                received_data = received_data.replace('END', '')
                break
    return received_data

while True:
    # Receive data from UART
    json_data = receive_json(ser)

    # Ensure the received data is not empty and is valid
    if json_data:
        try:
            # Convert JSON to a list of integers
            data_array = json.loads(json_data)
            # Print the received array
            print("Received array:", data_array)
            # Perform an operation on the integer array
            # Example: calculate the sum of the array elements
            array_sum = sum(data_array)
            # Print the result of the operation
            print("Sum of array elements:", array_sum)
            # Send confirmation of successful reception
            ser.write(b'OK')
            break
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No valid data received.")

# Close the serial port
ser.close()
