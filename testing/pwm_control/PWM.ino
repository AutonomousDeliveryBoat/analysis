#include <Servo.h>

byte servoPin = 9;
Servo servo;

void setup() {
  // initialize serial:
  Serial.begin(9600);
  servo.attach(servoPin);
  
  servo.writeMicroseconds(2000);
  delay(1000);
}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {

    int pwm = Serial.parseInt();
    

    // look for the newline. That's the end of your
    // sentence:
    if (Serial.read() == '\n') {
      servo.writeMicroseconds(pwm);
      Serial.print(pwm);
      Serial.print('\n');

    }
  }
}








