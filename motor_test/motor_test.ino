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
      analogWrite(MOTOR_1, 255);
      Serial.println("MOTOR 1");
    }

    if ((input_data & 0b010) == 0) {
      analogWrite(MOTOR_2, 0);
      Serial.println("MOTOR 2 OFF");
    } else {
      analogWrite(MOTOR_2, 255);
      Serial.println("MOTOR 2");
    }

    if ((input_data & 0b0100) == 0) {
      analogWrite(MOTOR_3, 0); 
      Serial.println("MOTOR 3 OFF");
    } else {
      analogWrite(MOTOR_3, 255);
      Serial.println("MOTOR 3");
    }

  }

}
