#define MOTOR_1 (5u)
#define MOTOR_2 (6u)
#define MOTOR_3 (9u)

void setup() {
  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);
  pinMode(MOTOR_3, OUTPUT);

  Serial.begin(9600);
  Serial.println("Select desired motor using position in binary:");
  Serial.println("EX. 1 = MOTOR1, 3=MOTOR1 + MOTOR2");
}

void loop() {
  if (Serial.available() > 0) {
    int input_data = Serial.read();

    if (input_data & 0b0001 == 0)
      analogWrite(MOTOR_1, 0);
    else
      analogWrite(MOTOR_1, 255);

    if (input_data & 0b0010 == 0)
      analogWrite(MOTOR_2, 0);
    else
      analogWrite(MOTOR_2, 255);

    if (input_data & 0b0100 == 0)
      analogWrite(MOTOR_3, 0); 
    else
      analogWrite(MOTOR_3, 255);

  }

}
