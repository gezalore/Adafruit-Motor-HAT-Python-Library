import time

from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM


class StepperMotor:

    step2coils = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, controller, num, steps=200, rpm=60):
        self.MC = controller
        self.dt = 60.0 / rpm / steps
        self.currentstep = 0

        if (num == 1):
            self.PWMA = 8
            self.AIN2 = 9
            self.AIN1 = 10
            self.PWMB = 13
            self.BIN2 = 12
            self.BIN1 = 11
        elif (num == 2):
            self.PWMA = 2
            self.AIN2 = 3
            self.AIN1 = 4
            self.PWMB = 7
            self.BIN2 = 6
            self.BIN1 = 5
        else:
            raise NameError('MotorHAT Stepper must be between 1 and 2 inclusive')

    def step(self, steps):
        # Turn channels full on!
        self.MC._pwm.setPWM(self.PWMA, 4096, 0)
        self.MC._pwm.setPWM(self.PWMB, 4096, 0)

        ds = 1 if steps > 0 else -1

        cs = self.currentstep + ds

        t = time.time()
        for cs in range(cs, cs + steps, ds):
            coils = StepperMotor.step2coils[cs % 4]

            self.MC.setPin(self.AIN2, coils[0])
            self.MC.setPin(self.BIN1, coils[1])
            self.MC.setPin(self.AIN1, coils[2])
            self.MC.setPin(self.BIN2, coils[3])

            t += self.dt

            while time.time() < t:
                pass

        self.currentstep = cs

class MotorHAT:

    def __init__(self, addr = 0x60, freq = 1600, i2c=None, i2c_bus=None):
        self._frequency = freq
        self._pwm = PWM(addr, debug=False, i2c=i2c, i2c_bus=i2c_bus)
        self._pwm.setPWMFreq(self._frequency)

    def setPin(self, pin, value):
        if (pin < 0) or (pin > 15):
            raise NameError('PWM pin must be between 0 and 15 inclusive')
        if (value != 0) and (value != 1):
            raise NameError('Pin value must be 0 or 1!')
        if (value == 0):
            self._pwm.setPWM(pin, 0, 4096)
        if (value == 1):
            self._pwm.setPWM(pin, 4096, 0)

    def releaseAll(self):
        for pin in (3, 4, 5, 6, 9, 10, 11, 12):
            self.setPin(pin, 0)
