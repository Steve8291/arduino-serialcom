#include <SerialCom.h>


SerialCom::SerialCom(uint8_t* recvArray, uint8_t recvArraySize) : recvArray(recvArray), recvArraySize(recvArraySize) {
}


// Returns the total number of bytes (dataSize) added to recvArray[]
// Decodes high bytes by adding specialByte
uint8_t SerialCom::recvData() {
  static bool recvInProgress = false;
  static bool decodeInProgress = false;
  static uint8_t index = 0;
  uint8_t dataSize = 0;
  uint8_t readByte;

  while (Serial.available() > 0 && dataSize == 0) {
      readByte = Serial.read();

    if (readByte == startMarker) {
      recvInProgress = true;
      decodeInProgress = false;
      index = 0;
    }
    else if (readByte == endMarker) {
      recvInProgress = false;
      dataSize = index;
    }
    else if (readByte == specialByte) {
      decodeInProgress = true;
    }
    else if (recvInProgress == true && index < recvArraySize) {
      if (decodeInProgress == true) {
        readByte = readByte + specialByte;
        decodeInProgress = false;
      }
      recvArray[index] = readByte;
      index++;
    }
    else {
      recvInProgress = false;
      decodeInProgress = false;
      index = 0;
    }
  }

  return dataSize;
}


// Sends data array along with start and end markers.
// Encodes all high bytes by subtracting specialByte.
void SerialCom::sendData(uint8_t* sendArray, uint8_t sendArraySize) {
  uint8_t sendByte;
  Serial.write(startMarker);

  for (uint8_t i=0; i < sendArraySize; i++) {
    sendByte = sendArray[i];
    if (sendByte >= specialByte) {
      sendByte = sendByte - specialByte;
      Serial.write(specialByte);
    }
    Serial.write(sendByte);
  }
  
  Serial.write(endMarker);
}

