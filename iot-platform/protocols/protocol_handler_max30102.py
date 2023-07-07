from typing import List, Dict
from utils import ResultMAX30102
# from .protocol_handler import ProtocolHandler
from .handler import Handler
from configs import ConfigMAX30102

from time import sleep
import RPi.GPIO as GPIO
from smbus2 import SMBus
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF

# register address-es
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

# currently not used
MAX_BRIGHTNESS = 255


class ProtocolHandlerMAX30102(Handler):
    def __init__(self, config: ConfigMAX30102) -> None:
        super().__init__("MAX30102", config)

    # by default, this assumes that physical pin 7 (GPIO 4) is used as interrupt
    # by default, this assumes that the device is at 0x57 on channel 1
    #def __init__(self, channel=1, address=0x57, gpio_pin=7):
        #print("Channel: {0}, address: {1}".format(channel, address))
        self.address = 0x57
        self.channel = config.channel
        self.bus = SMBus(self.channel)
        self.interrupt = config.gpio_pin

        # set gpio mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.interrupt, GPIO.IN)

        self.reset()

        sleep(1)  # wait 1 sec

        # read & clear interrupt register (read 1 byte)
        try:
            reg_data = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)
        except OSError:
            pass 
        # print("[SETUP] reset complete with interrupt register0: {0}".format(reg_data))
        self.setup()
        # print("[SETUP] setup complete")

    def close(self) -> None:
        self.shutdown()

    def shutdown(self) -> ResultMAX30102[bool]:
        """
        Shutdown the device.
        """
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x80])
        return ResultMAX30102[bool](passed=True, data=True, message="MAX30102 shutdown")

    def reset(self) -> ResultMAX30102[bool]:
        """
        Reset the device, this will clear all settings,
        so after running this, run setup() again.
        """
        try:
            self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x40])
        except OSError as e:
            return ResultMAX30102[bool](passed=False, data=False, message=f"Error while reseting module at '{self.address}'", error=e)
        return ResultMAX30102[bool](passed=True, data=True, message="MAX30102 reseted")

    def setup(self, led_mode=0x03) -> ResultMAX30102[bool]:
        """
        This will setup the device with the values written in sample Arduino code.
        """
        # INTR setting
        # 0xc0 : A_FULL_EN and PPG_RDY_EN = Interrupt will be triggered when
        # fifo almost full & new fifo data ready
        try:
            self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_1, [0xc0])
            self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_2, [0x00])

            # FIFO_WR_PTR[4:0]
            self.bus.write_i2c_block_data(self.address, REG_FIFO_WR_PTR, [0x00])
            # OVF_COUNTER[4:0]
            self.bus.write_i2c_block_data(self.address, REG_OVF_COUNTER, [0x00])
            # FIFO_RD_PTR[4:0]
            self.bus.write_i2c_block_data(self.address, REG_FIFO_RD_PTR, [0x00])

            # 0b 0100 1111
            # sample avg = 4, fifo rollover = false, fifo almost full = 17
            self.bus.write_i2c_block_data(self.address, REG_FIFO_CONFIG, [0x4f])

            # 0x02 for read-only, 0x03 for SpO2 mode, 0x07 multimode LED
            self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [led_mode])
            # 0b 0010 0111
            # SPO2_ADC range = 4096nA, SPO2 sample rate = 100Hz, LED pulse-width = 411uS
            self.bus.write_i2c_block_data(self.address, REG_SPO2_CONFIG, [0x27])

            # choose value for ~7mA for LED1
            self.bus.write_i2c_block_data(self.address, REG_LED1_PA, [0x24])
            # choose value for ~7mA for LED2
            self.bus.write_i2c_block_data(self.address, REG_LED2_PA, [0x24])
            # choose value fro ~25mA for Pilot LED
            self.bus.write_i2c_block_data(self.address, REG_PILOT_PA, [0x7f])
        except OSError as e:
            return ResultMAX30102[bool](passed=False, data=False, message=f"Failed to setup module at '{self.address}'", error=e)

        return ResultMAX30102[bool](passed=True, data=True, message="MAX30102 setup completed")

    # this won't validate the arguments!
    # use when changing the values from default
    def set_config(self, reg, value) -> ResultMAX30102[bool]:
        self.bus.write_i2c_block_data(self.address, reg, value)
        return ResultMAX30102[bool](passed=True, data=True, message="MAX30102 config set")

    def read_fifo(self) -> ResultMAX30102[dict]:
        """
        This function will read the data register.
        """
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        reg_INTR1 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)
        reg_INTR2 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_2, 1)

        # read 6-byte data from the device
        d = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 6)

        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

        return ResultMAX30102[dict](passed=True, data={"red": red_led, "ir": ir_led}, message="MAX30102 FIFO values")

    def read_sequential(self, amount=200) -> ResultMAX30102[dict]:
        """
        This function will read the red-led and ir-led `amount` times.
        This works as blocking function.
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            while(GPIO.input(self.interrupt) == 1):
                # wait for interrupt signal, which means the data is available
                # do nothing here
                pass

            red, ir = self.read_fifo()

            red_buf.append(red)
            ir_buf.append(ir)

        return ResultMAX30102[dict](passed=True, data={"red": red_buf, "ir": ir_buf}, message="MAX30102 sequential data")
