#ifndef SERIALCOM_H
#define SERIALCOM_H

#include <Arduino.h>


/*!
*   Controls serial communication using start byte 254 and end byte 255  
*   Uses 253 as a special byte to encode 253, 254, and 255  
*   Requires two parameters (recvArray, recvArraySize)  
*   Set recvArraySize to largest number of bytes you expect
*/
class SerialCom {
private:
  uint8_t* recvArray;
  const uint8_t recvArraySize;
  const uint8_t specialByte = 253;
  const uint8_t startMarker = 254;
  const uint8_t endMarker = 255;

public:
  SerialCom(uint8_t* recvArray, uint8_t recvArraySize);

  /*!
  *    Returns number of bytes received when endMarker is encountered.  
  *    Warning: calling recvData will always clear the byteArray.  
  *    Read your data from byteArray whenever (recvData > 0)  
  */
  uint8_t recvData();

  /*!
  *    Sends encoded data to PC  
  */
  void sendData(uint8_t* sendArray, uint8_t sendArraySize);
};


#endif