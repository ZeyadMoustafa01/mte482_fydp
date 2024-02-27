#include <ArduinoBLE.h>

#define MOTOR_1 (2u)
#define MOTOR_2 (3u)
#define MOTOR_3 (6u)

BLEService hFeedbackService("605C8890-D7F7-45D0-A3BA-953F59645E2D");
BLEByteCharacteristic dirCharacteristic("4A88F279-F65C-4ECC-8C95-04AC25142A83", BLERead | BLEWrite);

// Defined functions
void setup_ble();
void setup_motor();
void run_motor(uint8_t input_data);
void characteristicUpdated(BLEDevice central, BLECharacteristic thisChar);

bool wasConnected = true;

void setup() {
  Serial.begin(9600);
  while(!Serial);

  setup_ble();
  setup_motor();
}

void loop() {
  BLEDevice central = BLE.central();

  if (central && central.connected()) {
    if (!wasConnected) {
      wasConnected = true;
      Serial.print("Connected to central: ");
      Serial.println(central.address());
    }
  } else if (wasConnected) {
    wasConnected = false;
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }

  BLE.poll();

}

void run_motor(uint8_t input_data) {
  // Turn on motor based on motor bit position in input_data
  if ((input_data & 0b0001) == 0)
    analogWrite(MOTOR_1, 0);
  else
    analogWrite(MOTOR_1, 255);

  if ((input_data & 0b0010) == 0)
    analogWrite(MOTOR_2, 0);
  else
    analogWrite(MOTOR_2, 255);

  if ((input_data & 0b0100) == 0)
    analogWrite(MOTOR_3, 0); 
  else
    analogWrite(MOTOR_3, 255);

  delay(500);

  // Turn off all motors
  analogWrite(MOTOR_1, 0);
  analogWrite(MOTOR_2, 0);
  analogWrite(MOTOR_3, 0);

}

void characteristicUpdated(BLEDevice central, BLECharacteristic thisChar) {
  uint8_t value = 0;
  thisChar.readValue(value);

  Serial.print("The updated char is: ");
  Serial.print(value);
  Serial.println();
 
  run_motor(value);

}

void setup_ble() {
  if (!BLE.begin()) {
    Serial.println("Starting BLE module failed. Program stopping...");
    while(1);
  }

  BLE.setLocalName("Wristband");
  BLE.setAdvertisedService(hFeedbackService);

  hFeedbackService.addCharacteristic(dirCharacteristic);
  
  BLE.addService(hFeedbackService);

  dirCharacteristic.writeValue(0);

  dirCharacteristic.setEventHandler(BLEUpdated, characteristicUpdated);

  BLE.advertise();

  Serial.println("Bluetooth® device active, waiting for connections...");
}

void setup_motor() {
  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);
  pinMode(MOTOR_3, OUTPUT);
}
