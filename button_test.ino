#define BUTTON_1 10  // Pin for Firefox
#define BUTTON_2 7   // Pin for Discord
#define BUTTON_3 5   // Pin for Arduino IDE

void setup() {
  Serial.begin(9600);  // Start serial communication

  // Set button pins as input with internal pull-ups
  pinMode(BUTTON_1, INPUT_PULLUP);
  pinMode(BUTTON_2, INPUT_PULLUP);
  pinMode(BUTTON_3, INPUT_PULLUP);
}

void loop() {
  // Check if button 1 (Firefox) is pressed
  if (digitalRead(BUTTON_1) == LOW) {
    Serial.println("FIREFOX");
    delay(200);  // Debounce delay
  }

  // Check if button 2 (Discord) is pressed
  if (digitalRead(BUTTON_2) == LOW) {
    Serial.println("DISCORD");
    delay(200);  // Debounce delay
  }

  // Check if button 3 (Arduino IDE) is pressed
  if (digitalRead(BUTTON_3) == LOW) {
    Serial.println("ARDUINO");
    delay(200);  // Debounce delay
  }

  // Read potentiometer values
  int potValueA = analogRead(A0);
  int potValueB = analogRead(A1);

  // Map potentiometer value to LED brightness
  int ledBrightness = map(potValueA, 0, 1023, 0, 255);
  analogWrite(9, ledBrightness);  // Set LED brightness on pin 9

  // Send potentiometer data in CSV format
  Serial.print(potValueA);
  Serial.print(",");
  Serial.print(potValueB);

  delay(100);
}
