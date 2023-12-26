# arduino-serialcom
## Two-way serial communication between Arduino &amp; Python

This communication protocol allows sending all ascii and utf-8 characters/decimals from 0-255.  
Includes:  
- SerialCom - Arduino Library (Put this directory in your Arduino/libraries/)
  - serial_com.ino - example sketch
  - SerialCom.cpp  - implementation
  - SerialCom.h    - header file

- PythonSerial
  - example_serialcom.py - python example script
  - serialcom.py         - python module (needs to be in same directory as example_serialcom.py)
