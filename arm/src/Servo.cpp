#include <Arduino.h>
#include "Servo.h"


Servo::Servo (int channel, int min, int max, int idle) : servo_CHANNEL(channel), servo_MIN(min),
  servo_MAX(max), servo_IDLE(idle) {

}

int Servo::getAngle(){
  return servo_ANGLE;
}

void Servo::setAngle(int angleArg){
  if ( angleArg < 0) angleArg = 0;
  if ( angleArg > 180) angleArg = 180;

  int value = map(angleArg, 0, 179, servo_MIN, servo_MAX);
  pwm.setPWM(servo_CHANNEL, 0, value);

  servo_ANGLE = angleArg;
}

void Servo::goTo(int angleArg, int speed){
  int current_angle = servo_ANGLE;

  if(angleArg >= current_angle){
    for(int i=current_angle; i<angleArg; i++){
      this->setAngle(i);
      delay(speed);
    }
  }
  else{
    for(int i=current_angle; i>=angleArg; i--){
      this->setAngle(i);
      delay(speed);
    }
  }
}

void Servo::goToIdle(int speed){
  this->goTo(servo_IDLE, speed);
}
