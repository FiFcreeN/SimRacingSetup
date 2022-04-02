#define LEDS 12

int rpm[2];
int slash;
int j;
String stringRead;

const int buttonPin = 13;    // the number of the pushbutton pin

// Variables will change:
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

void setup() {
  //setup the Serial Monitor
  Serial.begin(9600);

  //prepare pins 2 -> 11
  for (int i = 2; i < LEDS; ++i) {
    pinMode(i, OUTPUT);
  }

  pinMode(buttonPin, INPUT_PULLUP);

}

void loop() {

  startAnimation();


  while (true) {
    //tiny delay for the serial port reading
    delay(5);

    //read the serial port STRING FORMAT TO PARSE: CURR_RPM/MAX_RPM/MIN_RPM
    if (Serial.available()) {
      stringRead = Serial.readStringUntil('\n');
    }

    //turn off the lights
    else {
      stringRead = "0/0";
    }

    //reset the indexes of the slashes on the string
    slash = 0;

    //get the substring indexes
    for (int i = 0; stringRead[i] != '\0'; ++i) {

      //get the slashes on the srting rpm/max/min position
      if (stringRead[i] == '/') {
        slash = i;
        break;
      }
    }

    //define each param of rpm necessary to light the leds
    rpm[0] = stringRead.substring(0, slash).toInt();
    rpm[1] = stringRead.substring(slash + 1).toInt();

    //light up the leds with the given info
    rpmLeds(rpm[0], rpm[1]);



    // read the state of the switch into a local variable:
    int reading = !digitalRead(buttonPin);

    // check to see if you just pressed the button
    // (i.e. the input went from LOW to HIGH), and you've waited long enough
    // since the last press to ignore any noise:

    // If the switch changed, due to noise or pressing:
    if (reading != lastButtonState) {
      // reset the debouncing timer
      lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
      // whatever the reading is at, it's been there for longer than the debounce
      // delay, so take it as the actual current state:

      // if the button state has changed:
      if (reading != buttonState) {
        buttonState = reading;

        // only toggle the LED if the new button state is HIGH
        if (buttonState == HIGH) {
          Serial.print("X\n");
        }
        else {
          Serial.print("Y\n");
        }
      }
    }

    // save the reading. Next time through the loop, it'll be the lastButtonState:
    lastButtonState = reading;

  }
}

/*
 * Turns on all the leds to check if they are working when the program starts
 */
void startAnimation() {
  //animation to check led functioning
  for (int i = 2; i < LEDS; ++i) {
    digitalWrite(i, HIGH);
    delay(100);
  }

  for (int i = LEDS - 1; i > 1; --i) {
    digitalWrite(i, LOW);
    delay(100);
  }
}


/*
   Lights up a sequence of ten leds connected from pins 2 -> 11

   args:
    currMPM: the rpm of the car
    maxRPM: the maximum rpm of the car
*/
void rpmLeds(int currRPM, int maxRPM) {
  if (currRPM * maxRPM == 0) {
    return;
  }

  //calculate which leds to light up
  float rpm = currRPM - (maxRPM * 0.9 * 0.65);
  int RPMrange = maxRPM - (maxRPM * 0.65);

  int leds = (rpm / RPMrange) * 10;

  //light the corresponding leds
  for (int i = 0; i < LEDS; ++i) {
    digitalWrite(i + 2, i < leds);
  }

}
