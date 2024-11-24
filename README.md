# Description

This project is sa toy for those interested in learning how morse code works. It has an led that blinks following the morse code protocol and a display that shows which character is currently being transmitted. The objective is to decode the phrase being transmitted (ideally not looking at the display).

## Hardware

This proyect uses a discontinued esp32-s3 based development board, an yellow led and a lcd display of 2 rows and 16 collumns with an i2c backpack.

## Software

The code is pretty simple, in the codeled file is a class that contains a dictionary that matches each letter with it's respective morse code representation. Then it has a function called tx which can be passed two parameters, a string that contains the message to transmit and a reference time which is the dot representation time (all other times are multiples of this one).

Then on the code.py file there is a hardcoded message, the class is instantiated and the function is call with the message.

## Demo:

https://github.com/user-attachments/assets/bfef846b-3994-4e8d-9b5a-6cedf1874253

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
