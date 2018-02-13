#ifndef SERVO_H
#define SERVO_H

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

static Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

class Servo {
  public:
    Servo(int channel, int min, int max, int idle);
    int getAngle();
    void setAngle(int angleArg);
    void goTo(int angleArg, int speed);
    void goToIdle(int speed);

  private:
    int servo_CHANNEL = 0;
    int servo_MIN = 180;
    int servo_MAX = 500;
    int servo_IDLE = 90;
    int servo_ANGLE = 0;
};

#endif
