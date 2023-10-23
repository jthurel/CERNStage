import serial

# Define the serial port and its parameters
serial_port = '/dev/ttyUSB0'
baud_rate = 9600

try:
    with serial.Serial(serial_port, baud_rate, timeout=2) as ser:
        print(f"Connected to {serial_port} at {baud_rate} baud.")

        # Send data to the device
        #data_to_send = "Hello, device!\r\n"
        #ser.write(data_to_send.encode('utf-8'))

        # Read data from the device
        #received_data = ser.readline().decode('utf-8')
        #print(f"Received data: {received_data}")

except serial.SerialException as e:
    print(f"Error: {e}")