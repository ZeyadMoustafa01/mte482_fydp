#define MOTOR_1 (2u)
#define MOTOR_2 (3u)
#define MOTOR_3 (6u)

void setup() {
  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);
  pinMode(MOTOR_3, OUTPUT);

  Serial.begin(9600);
  while(!Serial);
  Serial.println("Select desired motor using position in binary:");
  Serial.println("EX. 1 = MOTOR1, 3=MOTOR1 + MOTOR2");
}

void runMotor(uint8_t num) {
  for (uint8_t i = 0; i < num; i++) {
    analogWrite(MOTOR_3, 255);
    delay(250);
    analogWrite(MOTOR_3, 0);
    delay(150);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int input_data = Serial.read();
    Serial.read();
    input_data %= 48;
    Serial.print("Input data: ");
    Serial.println(input_data);

    if ((input_data & 0b001) == 0) {
      analogWrite(MOTOR_1, 0);
      Serial.println("MOTOR 1 OFF");
    } else {
      // analogWrite(MOTOR_1, 155);
      // Serial.println("MOTOR 1");
      runMotor(1);
      Serial.println("RIGHT");
    }

    if ((input_data & 0b010) == 0) {
      analogWrite(MOTOR_2, 0);
      Serial.println("MOTOR 2 OFF");
    } else {
      // analogWrite(MOTOR_2, 155);
      // Serial.println("MOTOR 2");
      runMotor(2);
      Serial.println("CENTRE");
    }

    if ((input_data & 0b0100) == 0) {
      analogWrite(MOTOR_3, 0); 
      Serial.println("MOTOR 3 OFF");
    } else {
      // analogWrite(MOTOR_3, 155);
      // Serial.println("MOTOR 3");
      runMotor(3);
      Serial.println("LEFT");
    }

  }

}
