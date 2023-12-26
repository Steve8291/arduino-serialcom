import serialcom
import time


port = '/dev/cu.usbmodem141224101'
port = 'arduino'

arduino_com = serialcom.SerialCom(port, 115200)
time.sleep(3)  # Arduino resets with a new serial connection.
# https://arduino.stackexchange.com/questions/20426/how-to-stop-arduino-from-reseting-after-serial-connection-lost
# https://raspberrypi.stackexchange.com/questions/9695/disable-dtr-on-ttyusb0/31298#31298


print('\n______ Serial connection info ______')
print(arduino_com)

print('\n______ Device Info ______')
# Returns 'None' if not connected.
# Can be used to test if connectivity was lost.
print(arduino_com.device_info)

print('\n______ First port matching an Arduino ______')
print(serialcom.get_arduino_port())

print('\n______ List of all active serail ports ______')
ports = serialcom.list_ports()
for i in ports:
    print(i)


value_a = 'ABC'                     # ASCII string
value_b = 0xAE                      # single hex value
value_c = [65, 66, 67]              # list of decimal ints
value_d = [0x41, 0x42, 0x43, 0x9A]  # list of hex ints
value_e = bytes(value_a, 'utf-8')   # convert string to bytes obj
value_f = bytearray(value_d)        # bytearray
value_g = (65, 66, 67)              # tuple
value_h = {65, 66, 255}             # set

# Uncomment to test values:
arduino_com.write_data(value_a)
# arduino_com.write_data(value_b)
# arduino_com.write_data(value_c)
# arduino_com.write_data(value_d)
# arduino_com.write_data(value_e)
# arduino_com.write_data(value_f)
# arduino_com.write_data(value_g)
# arduino_com.write_data(value_h)

# recv_buffer is a list of bytearray objects.
# Here we iterate the list and print the entire bytearray.
# Loop to keep program open long enough to receive response from Arduino
# Arduino serialcom example will send back whatever you write to it.
t_end = time.time() + 5
while time.time() < t_end:
    if len(arduino_com.recv_buffer) > 0:
        print('\n______ Printing recv_buffer ______')
        new_message = arduino_com.recv_buffer.pop(0)
        print(new_message)  # bytearray object
        print(new_message.decode('utf-8'))
        for i in new_message:
            print(i)  # Iterating a bytearray returns an int
