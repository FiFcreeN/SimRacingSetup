#define LEDS 12

int rpm[2];
int slash;
int j;
String stringRead;

void setup() {
  //setup the Serial Monitor
  Serial.begin(9600);

  //prepare pins 2 -> 11
  for (int i = 2; i < LEDS; ++i) {
    pinMode(i, OUTPUT);
  }

}

void loop() {
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

}


/*
   Lights up a sequence of ten leds connected from pins 2 -> 11

   args:
    currMPM: the rpm of the car
    maxRPM: the maximum rpm of the car
*/
void rpmLeds(int currRPM, int maxRPM) {
  if (currRPM * maxRPM == 0) {
    for (int i = 0; i < LEDS; ++i) {
      digitalWrite(i + 2, LOW);
    }
    return;
  }

  //calculate which leds to light up
  float rpm = currRPM - (maxRPM * 0.9 * 0.65);
  int RPMrange = maxRPM - (maxRPM * 0.65);

  int leds = (rpm / RPMrange) * 10;

  //light the corresponding leds
  for (int i = 0; i < leds; ++i) {
    digitalWrite(i + 2, HIGH);
  }

}
