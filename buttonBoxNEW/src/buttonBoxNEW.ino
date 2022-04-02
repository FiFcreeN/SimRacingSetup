#define CLK 2
#define DT 3
#define SW 4
#define DEBOUNCE_DELAY 50
#define BUTTON_DELAY 100

//rotor
int currentStateCLK;
int lastStateCLK;

unsigned long debounceAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

//matrizes de estados
int leituraAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int estadosAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int lastEstadoAlavancas[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void setup() {
  //ENCODER
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);

  //LEDS
  pinMode(A3, OUTPUT);
  pinMode(A5, OUTPUT);

  //START THE SERIAL MONITOR
  Serial.begin(9600);

  //INITIALIZE
  lastStateCLK = digitalRead(CLK);

  //setup the button pins (3 -> 13)
  for (int i = 5; i < 14; ++i) {
    pinMode(i, INPUT_PULLUP);
  }
}

void loop() {
  //rotor
  currentStateCLK = digitalRead(CLK);

  if (currentStateCLK != lastStateCLK) {

    if (digitalRead(DT) != currentStateCLK) {
      Serial.println("R");
    }

    if (digitalRead(DT) == currentStateCLK) {
      Serial.println("L");
    }
  }



  //BOTOES NORMAIS

  for (int i = 4; i < 14; ++i) {
    leituraAlavancas[i - 4] = !digitalRead(i);
  }

  digitalWrite(A3, leituraAlavancas[8]);
  digitalWrite(A5, leituraAlavancas[9]);


  //DEBOUNCE EVERY BUTTON
  for (int i = 0; i < 10; ++i) {
    if (leituraAlavancas[i] != lastEstadoAlavancas[i]) {
      debounceAlavancas[i] = millis();
    }
    if ((millis() - debounceAlavancas[i]) > DEBOUNCE_DELAY) {
      if (leituraAlavancas[i] != estadosAlavancas[i]) {
        estadosAlavancas[i] = leituraAlavancas[i];

        if (estadosAlavancas[i]) {
          Serial.println(String(i));
          delay(BUTTON_DELAY);
        } else if ((i == 1 || i == 2 || i > 6 && i < 10) && !estadosAlavancas[i]) {
          Serial.println(String(i));
          delay(BUTTON_DELAY);
        }
      }
    }
    lastEstadoAlavancas[i] = leituraAlavancas[i];
  }

  lastStateCLK = currentStateCLK;
}
