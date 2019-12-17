
from time import sleep
import RPi.GPIO as GPIO
import sys

DIR = 20 # direction pin
STEP = 21
DIR2 = 19 # direction pin
STEP2 = 26
CW = 1
CCW = 0
SPR = 200 # Steps per rotation.

ENABLE = 13
ENABLE2 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.output(DIR, CW)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.output(DIR2, CCW)

GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(ENABLE, False)
GPIO.setup(ENABLE2, GPIO.OUT)
GPIO.output(ENABLE2, False)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
MODE2 = (17, 27, 22)   # Microstep Resolution GPIO Pins

GPIO.setup(MODE, GPIO.OUT)
GPIO.setup(MODE2, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (1, 1, 1)}

DELAYS = {'Full': .001,
              'Half': .0005,
              '1/4': .000125,
              '1/8': .000125,
              '1/16': .00001}
SETTING = '1/4'
res = RESOLUTION[str(SETTING)]
GPIO.output(MODE, res)
GPIO.output(MODE2, res)

step_count = 200 * 32
if len(sys.argv) >= 2:
	step_count = int(sys.argv[1])

delay = DELAYS[str(SETTING)]
print delay

GPIO.output(ENABLE, True)
GPIO.output(ENABLE2, True)
# Sleepwake delay
sleep(.1)

for x in range(step_count):
	GPIO.output(STEP, GPIO.HIGH)
	GPIO.output(STEP2, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	GPIO.output(STEP2, GPIO.LOW)
	sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
GPIO.output(DIR2, CW)
for x in range(step_count):
	GPIO.output(STEP, GPIO.HIGH)
	GPIO.output(STEP2, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	GPIO.output(STEP2, GPIO.LOW)
	sleep(delay)

GPIO.output(ENABLE, False)
GPIO.output(ENABLE2, False)

# GPIO.cleanup()


# from time import sleep
# import pigpio

# DIR = 20     # Direction GPIO Pin
# STEP = 21    # Step GPIO Pin
# DIR2 = 19 # direction pin
# STEP2 = 26
# SWITCH = 16  # GPIO pin of switch

# # Connect to pigpiod daemon
# pi = pigpio.pi()

# # Set up pins as an output
# pi.set_mode(DIR, pigpio.OUTPUT)
# pi.set_mode(STEP, pigpio.OUTPUT)
# pi.set_mode(DIR2, pigpio.OUTPUT)
# pi.set_mode(STEP2, pigpio.OUTPUT)


# # Set up input switch
# pi.set_mode(SWITCH, pigpio.INPUT)
# pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

# MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
# MODE2 = (17, 27, 22)   # Microstep Resolution GPIO Pins
# RESOLUTION = {'Full': (0, 0, 0),
#               'Half': (1, 0, 0),
#               '1/4': (0, 1, 0),
#               '1/8': (1, 1, 0),
#               '1/16': (0, 0, 1),
#               '1/32': (1, 0, 1)}
# for i in range(3):
#     pi.write(MODE[i], RESOLUTION['1/32'][i])
#     pi.write(MODE2[i], RESOLUTION['1/32'][i])

# # Set duty cycle and frequency
# pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off
# pi.set_PWM_frequency(STEP, 1250)  # 500 pulses per second
# # pi.set_PWM_dutycycle(STEP2, 128)  # PWM 1/2 On 1/2 Off
# # pi.set_PWM_frequency(STEP2, 1250)  # 500 pulses per second
# pi.write(DIR2, 0)  # Set direction


# try:
#     while True:
#         pi.write(DIR, pi.read(SWITCH))  # Set direction
#         pi.write(DIR2, pi.read(not SWITCH))  # Set direction
#         sleep(.1)

# except KeyboardInterrupt:
#     print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
# finally:
#     pi.set_PWM_dutycycle(STEP, 0)  # PWM off
#     pi.set_PWM_dutycycle(STEP2, 0)  # PWM off
#     pi.stop()