#include <Arduino.h>
#include <Wire.h>
#include "Servo.h"

void test_servos(int speed);
void applyStickPosition(int pin, Servo* servo);

#define STICK_THRESHOLD 500
#define STICK_MIDLE 2048
// Stick pins
#define STICK_PALONIER 0
#define STICK_EPAULE 1
#define STICK_COUDE 2
#define STICK_COUDE_ROT 3
#define STICK_POIGNET 4
#define STICK_POIGNET_ROT 5
#define STICK_GRIP 6

// Driver channels
#define CH_SERV_PALONIER 0
#define CH_SERV_EPAULE 1
#define CH_SERV_COUDE 2
#define CH_SERV_COUDE_ROT 3
#define CH_SERV_POIGNET 4
#define CH_SERV_POIGNET_ROT 5
#define CH_SERV_GRIP 6

Servo SERVO_PALONIER = Servo(CH_SERV_PALONIER, 110, 530, 90);
Servo SERVO_EPAULE = Servo(CH_SERV_EPAULE, 180, 480, 10);
Servo SERVO_COUDE = Servo(CH_SERV_COUDE, 300, 550, 100);
Servo SERVO_COUDE_ROT = Servo(CH_SERV_COUDE_ROT, 110, 550, 90);
Servo SERVO_POIGNET = Servo(CH_SERV_POIGNET, 110, 480, 60);
Servo SERVO_POIGNET_ROT = Servo(CH_SERV_POIGNET_ROT, 100, 500, 90);
Servo SERVO_GRIP = Servo(CH_SERV_GRIP, 180, 320, 0);

void setup() {
  pwm.begin();
  pwm.setPWMFreq(60);
  yield();

  SERVO_PALONIER.setAngle(90);
  SERVO_EPAULE.setAngle(10);
  SERVO_COUDE.setAngle(100);
  SERVO_COUDE_ROT.setAngle(90);
  SERVO_POIGNET.setAngle(90);
  SERVO_POIGNET_ROT.setAngle(90);
  SERVO_GRIP.setAngle(90);
  delay(500);
}

void loop() {
  applyStickPosition(STICK_PALONIER, &SERVO_PALONIER);
  applyStickPosition(STICK_EPAULE, &SERVO_EPAULE);
  applyStickPosition(STICK_COUDE, &SERVO_COUDE);
  applyStickPosition(STICK_COUDE_ROT, &SERVO_COUDE_ROT);
  applyStickPosition(STICK_POIGNET, &SERVO_POIGNET);
  applyStickPosition(STICK_POIGNET_ROT, &SERVO_POIGNET_ROT);
  applyStickPosition(STICK_GRIP, &SERVO_GRIP);

  delay(10);
}

void applyStickPosition(int pin, Servo* servo){
  int analog_value = analogRead(pin);
  int current = servo->getAngle();

  if(analog_value > (STICK_MIDLE + STICK_THRESHOLD)){
    int target = current + 1;

    if( target <= 180 ){
      servo->setAngle(target);
    }
  }
  else if (analog_value < (STICK_MIDLE - STICK_THRESHOLD)){
    int target = current - 1;

    if( target >= 0 ){
      servo->setAngle(target);
    }
  }
}

void test_servos(int speed){
  SERVO_EPAULE.setAngle(20);
  SERVO_COUDE.setAngle(30);

  SERVO_PALONIER.goTo(180, speed*2);
  delay(500);
  SERVO_PALONIER.goTo(0, speed*2);
  delay(500);
  SERVO_PALONIER.goToIdle(speed*2);
  delay(500);

  SERVO_EPAULE.goTo(150, speed*2);
  delay(500);
  SERVO_EPAULE.goTo(20, speed*2);
  delay(500);

  SERVO_COUDE.goTo(180, speed);
  delay(500);
  SERVO_COUDE.goTo(30, speed);
  delay(500);

  SERVO_COUDE_ROT.goTo(180, speed);
  delay(500);
  SERVO_COUDE_ROT.goTo(0, speed);
  delay(500);
  SERVO_COUDE_ROT.goToIdle(speed);
  delay(500);

  SERVO_POIGNET.goTo(180, speed);
  delay(500);
  SERVO_POIGNET.goTo(0, speed);
  delay(500);
  SERVO_POIGNET.goToIdle(speed);
  delay(500);

  SERVO_POIGNET_ROT.goTo(180, speed);
  delay(500);
  SERVO_POIGNET_ROT.goTo(0, speed);
  delay(500);
  SERVO_POIGNET_ROT.goToIdle(speed);
  delay(500);

  SERVO_GRIP.goTo(180, speed);
  delay(500);
  SERVO_GRIP.goToIdle(speed);
  delay(500);
}
