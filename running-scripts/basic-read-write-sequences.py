import serial
# Read / Write basic sequences.

# specify 19200 bauds
# check interest of rts?
# yes for ascii decode
#with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
#    ser.rts = True
#    ser.write(bytes("*RST", 'utf-8') + b'\r')
#    ser.close()

with serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=2) as ser:
    ser.rts = True
    ser.reset_input_buffer()
    ser.write(bytes("*IDN?", 'utf-8') + b'\r')
    response = ser.readline().decode('ascii')
    print (response)

    # command without error (0)
    ser.write(bytes("AMPLIT, 1.9", 'utf-8') + b'\r')
    ser.write(bytes("*ESR?", 'utf-8') + b'\r')
    response = ser.readline().decode('ascii')
    print (response)

    # command with error (16 <> 0)
    ser.write(bytes("AMPLIT, 19", 'utf-8') + b'\r')
    ser.write(bytes("*ESR?", 'utf-8') + b'\r')
    response = ser.readline().decode('ascii')
    print (response)