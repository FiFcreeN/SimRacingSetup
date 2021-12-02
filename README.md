# SimRacingSetup

Some programs to ease the making of a "DIY" sim racing setup 


## Objective

Create apps to use arduino uno as a interpreter for sim racing gadgets.

## Files

**HANDBRAKE Files**
```handbrake.ino``` - can be uploaded to arduino (uno) reads the state of a button (INPUT_PULLUP enabled) connected on pin 13 and outputs a message on the serial port corresponding to the current state of the button
```handbrake.py``` - reads the arduino uno serial port and whenever it detects an input, from the button connected to the arduino, simulates the keypress of the "p" key


**REV LIGHTS Files:** ***sketch under development***
```revLights.ino```  - can be uploaded to a arduino (uno). Used to light a series of LEDs connected from pin 2 to 11 (with proper resistors [330ohm])
```serial.py``` - used to select the serial port on which the arduino is connected and is currently being used for testing the LED sketch


## Under investigation

Currently investigating how to read inputs from an UDP server in a sim racing game

**FORZA GAMES** - [https://github.com/nettrom/forza_motorsport] - repository with some porgrams to get data from the forza data out udp feature.


## Phisical components

**Handbrake** - a misc between Mecano parts, a wooden broomstick segment and a bycicle ruber handle and a pushbutton.

**Rev Lights** - 4 green LEDs, 4 yellow LEDs, 2 red LEDs, a 220 ohm resistor. Mounted into a black painted pine wood segment.

**Button Box** - A set of 3 lever switches, 5 pushbuttons and a "normal" switch. Mounted on a black painted pine wood box.

**NOTE:** *I will not post any pictures because my craftsmanship is terrible :(*
