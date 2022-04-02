//debounce delay
unsigned long debounceDelay = 50;
unsigned long debounceAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

//matrizes de estados
int leituraAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int estadosAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int lastEstadoAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void setup() {
  //start the serial comunication channel
  Serial.begin(9600);
  
  //setup the led pins
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  
  //setup the button pins (3 -> 13)
  for (int i = 3; i < 13; ++i){
    if (i != 9) pinMode(i, INPUT_PULLUP);
  }


}

void loop() {
  for (int i = 0; i < 6; ++i) {
    leituraAlavancas[i] = !digitalRead(i + 3);
  }
  for (int i = 7; i < 11; ++i) {
    leituraAlavancas[i-1] = !digitalRead(i + 3);
  }

  digitalWrite(2, estadosAlavancas[8]);
  digitalWrite(9, estadosAlavancas[9]);

  for (int i = 0; i < 10; ++i) {
    if (i == 3 || i == 3) {
      continue;
    }
    if (leituraAlavancas[i] != lastEstadoAlavancas[i]) {
      debounceAlavancas[i] = millis();
    }
    if ((millis() - debounceAlavancas[i]) > debounceDelay) {
      if (leituraAlavancas[i] != estadosAlavancas[i]) {
        estadosAlavancas[i] = leituraAlavancas[i];

        if (i == 0 || i > 3 && i < 7) {
          if (estadosAlavancas[i]) {
            Serial.println(String(i));
            delay(300);
          }
        }
        else if (i == 1) {
          if (estadosAlavancas[1] && leituraAlavancas[2]) {
            Serial.println("L");
            delay(150);
          }
          else if (estadosAlavancas[1] && leituraAlavancas[3]) {
            Serial.println("R");
            delay(150);
          }
          else if (estadosAlavancas[1] && (!leituraAlavancas[2] && !leituraAlavancas[3])) {
            Serial.println(String(i));
            delay(150);
          }
        }
        else if (i != 5 && i >= 7) {
          Serial.println(String(i));
          delay(150);
        }
      }
    }
    lastEstadoAlavancas[i] = leituraAlavancas[i];
  }
}
