import serial
ser = serial.Serial(port= "ttyS0", baudrate=115200,timeout=1)
ser.open()
ser.write(bytes(AMPLIT,0.5, 'UTF-8') + b'\r')

ser.close()