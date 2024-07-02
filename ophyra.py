import machine
import ujson
import urandom
import time

# Create an array of 1000 data points
data = [urandom.randint(0, 100) for _ in range(1000)]

# Convert the array to JSON
json_data = ujson.dumps(data)


# Function to split JSON into manageable chunks
def split_string(s, chunk_size):
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


# Calculate chunk size (65% of transmission capacity at 115200 baud)
baud_rate = 115200
bytes_per_second = baud_rate // 8
chunk_size = int(bytes_per_second * 0.65)  # 65% of transmission capacity

# Split JSON into manageable chunks
chunks = split_string(json_data, chunk_size)

# Initialize UART2 serial communication
uart = machine.UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

while True:
    # Send chunks through UART
    for chunk in chunks:
        uart.write(chunk)
        time.sleep(0.1)  # Adjust the wait time as necessary

    # Send an end marker
    uart.write(b'END')

    # Wait for confirmation of successful reception
    start_time = time.ticks_ms()
    confirmed = False
    while time.ticks_diff(time.ticks_ms(), start_time) < 3000:
        if uart.any():
            response = uart.read()
            if response == b'OK':
                print("Reception confirmed, closing connection.")
                confirmed = True
                break

    if confirmed:
        break
    else:
        print("Timeout, retrying data transmission.")
