#include <ArduinoBLE.h>

BLEService hFeedbackService("605C8890-D7F7-45D0-A3BA-953F59645E2D");
BLEByteCharacteristic dirCharacteristic("4A88F279-F65C-4ECC-8C95-04AC25142A83", BLERead | BLEWrite);

bool wasConnected = true;

void setup() {
  Serial.begin(9600);
  while(!Serial);

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

void loop() {
  // put your main code here, to run repeatedly:
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

void characteristicUpdated(BLEDevice central, BLECharacteristic thisChar) {
  uint8_t value = 0;
  thisChar.readValue(value);
  Serial.print("The updated char is: ");
  Serial.print(value);
  Serial.println();
}


