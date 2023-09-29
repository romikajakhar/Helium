import serial

success = 0
failed = 0
ser=serial.Serial('COM4', 115200, write_timeout=10)
rssi_list=[]

for i in range(5):
    command ='AT+SEND=1:11223344556677889900aa\r'
    sendCommand = command.encode()
    ser.write(sendCommand)
ser.timeout = 1
msg = ser.read(size=1024)
print(msg)
ser.timeout = 30
msg = ser.read(size=1024)
output = str(msg, 'UTF-8')
print(output)
if 'CONFIRMED_OK' in output:
    print('successful transmission')
    success+=1
    command_rssi = 'AT+RSSI=?\r'
    ser.write(send_rssi)
    send_rssi = command_rssi.encode()
    ser.timeout = 1
    msg = ser.read(size=1024)
    print(msg)
    ser.timeout = 30
    msg = ser.read(size=1024)
    output = str(msg, 'UTF-8')
    print(output)
    rssi_list.append(output)

     
elif 'FAILED' in output:
    print('failed transmission')
    failed+=1
     

print('successful transmission count is', success)
print('failed transmission count is', failed)
print(rssi_list)
ser.close()