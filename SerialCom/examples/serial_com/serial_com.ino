#include <SerialCom.h>

// Create array that is as large as the largest message you will receive.
// Array may be as large as you like but will take up more memory.
// Any incoming message larger than the array will be droppped.
// This library must be used with the complimentary Python library on a PC.
// Only one serial monitor can receive at a time.
// To what is being received here, you can open the Arduino IDE serial monitor
// quickly after starting the Python app.

static uint8_t myArray[10];
SerialCom mySerialObj(myArray, 10);

void setup() {
  Serial.begin(115200);
}

void loop() {
  uint8_t dataSize = mySerialObj.recvData();

  // ASCI Tables: https://www.rapidtables.com/code/text/ascii-table.html
  // Send "HELLO!"
  uint8_t helloMsg[6] = {'H','E', 76, 0x4C, 0x4F, '!'};

  if (dataSize > 0) {
    Serial.write("____ Iterate Through Array ____");

    for (int i = 0; i < dataSize; i++) {
      Serial.write("\nIndex: ");
      Serial.print(i);
      Serial.write("\nValue: ");
      Serial.write(myArray[i]);
      Serial.write("\n");
    }

    Serial.println("\n____ Print Entire Array ____");
    Serial.write("myArray: ");
    Serial.write(myArray, sizeof(myArray));
    Serial.write("\n\n");

    Serial.println("____ Send helloMsg Array ____");
    Serial.write("Size of helloMsg Array: ");
    Serial.print(sizeof(helloMsg));
    Serial.write("\n");
    mySerialObj.sendData(helloMsg, sizeof(helloMsg));
    mySerialObj.sendData(myArray, dataSize);
  }

}