import asyncio
import board
import digitalio
import busio
import touchio
import microcontroller
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

class CodeLed():
    
    def __init__(self, output, i2c) -> None:
        self._led = digitalio.DigitalInOut(output) # board.IO41 = onboard _led / board.IO9 = 3er pin

        self._led.direction = digitalio.Direction.OUTPUT
        self.i2c = i2c
        cols = 16
        rows = 2
        
        self.restart_btn = touchio.TouchIn(board.IO6)
        self.show_btn = touchio.TouchIn(board.IO7)
        
        print("restart value:" + str(self.restart_btn.raw_value))
        print("show value:" + str(self.show_btn.raw_value))
        self.restart_btn.threshold = 40000
        self.show_btn.threshold = 50000
        try:
            self.lcd = LCD(I2CPCF8574Interface(self.i2c, 0x27), num_rows=rows, num_cols=cols)
        except:        
            self.lcd = None                
    MORSE_CODE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.',
        'H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','Ñ':'-.-.--',
        'O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-',
        'V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
        '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
        '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
        '.':'.-.-.-',
        ',':'--..--',
        '?':'..--..',
        '/':'--..-.',
        '@':'.--.-.',
        ' ':' ',
    }

    BRAILLE_CODE = {
    'a': '100000',
    'b': '110000',
    'c': '100100',
    'd': '100110',
    'e': '100010',
    'f': '110100',
    'g': '110110',
    'h': '110010',
    'i': '010100',
    'j': '010110',
    'k': '101000',
    'l': '111000',
    'm': '101100',
    'n': '101110',
    'o': '101010',
    'p': '111100',
    'q': '111110',
    'r': '111010',
    's': '011100',
    't': '011110',
    'u': '101001',
    'v': '111001',
    'w': '010111',
    'x': '101101',
    'y': '101111',
    'z': '101011',
    '#': '001111',
    '1': '100000',
    '2': '110000',
    '3': '100100',
    '4': '100110',
    '5': '100010',
    '6': '110100',
    '7': '110110',
    '8': '110010',
    '9': '010100',
    '0': '010110',
    ' ': '000000'}
    async def blink(self, period_ms):
        while True:
            self._led.value = True
            await asyncio.sleep_ms(100)
            self._led.value = False
            await asyncio.sleep_ms(period_ms)

    async def flash(self,uptime,lowtime):
        self._led.value = True
        await asyncio.sleep_ms(uptime)
        self._led.value = False
        await asyncio.sleep_ms(lowtime)
        return

    async def tx(self, code = "MORSE", msg="SOS",t_ref = 500):
        self.lcd.clear()
        if code == "MORSE":
            tdot = t_ref
            tdash = tdot * 3
            tword = tdot * 6

            i = 0
            if self.lcd is not None:
                self.lcd.clear()
                self.lcd.set_backlight(True)
            for l in msg:
                char = self.MORSE_CODE.get(l.upper())
                if self.lcd is not None and char is not None:
                    self.lcd.clear()
                    self.lcd.set_cursor_pos(0, 0)
                    #self.lcd.print(l)
                    self.lcd.set_cursor_pos(1, 0)
                    self.lcd.print(char)
                    i += 1
                    for symbol in char:
                        if symbol==".":
                            await self.flash(tdot,tdot)
                        if symbol=="-":
                            await self.flash(tdash,tdot)
                        if symbol==" ":
                            await asyncio.sleep_ms(tword)   
                await asyncio.sleep_ms(tdash)        
        elif code == "BRAILLE":
            if self.lcd is not None:
                self.lcd.clear()
                self.lcd.set_backlight(True)
            for l in msg:
                if self.lcd is not None:
                    self.lcd.clear()
                char = self.BRAILLE_CODE.get(l.lower())
                up = char[3:]
                down = char[:3]
                for i,symbol in enumerate(up):
                    if self.lcd is not None:
                        self.lcd.set_cursor_pos(0, i)
                    point = "." if symbol == '1' else ""
                    if self.lcd is not None:
                        self.lcd.print(point)
                for i,symbol in enumerate(down):
                    if self.lcd is not None:
                        self.lcd.set_cursor_pos(1, i)
                    point = "." if symbol == '1' else ""
                    if self.lcd is not None:
                        self.lcd.print(point)
                if self.lcd is not None:                    
                    self.lcd.set_cursor_pos(0, 15)
                    self.lcd.print(l)
                await asyncio.sleep_ms(t_ref)
        else:
            pass
        
    async def restart_game(self):
        self.lcd.clear()
        self.lcd.set_cursor_pos(0, 0)
        self.lcd.print("Iniciar")
        while not self.restart_btn.value:
            await asyncio.sleep_ms(50)
            
    async def show_msg(self):
        self.lcd.clear()
        self.lcd.set_cursor_pos(1, 0)
        self.lcd.print("Mostrar")    
        while not self.show_btn.value:
            await asyncio.sleep_ms(50)
            
    async def count_2_reset(self):
        count = 0
        while True:
            if self.restart_btn.value:
                print(count)
                count += 1
            if count > 10:
                await asyncio.sleep_ms(1000)
                microcontroller.reset()
            await asyncio.sleep_ms(200)
            
    async def print_msg(self, msg_original):
        msg = remove_non_alpha(msg_original) 
        while True:           
            if(len(msg)>=16):
                for i in range(len(msg) - 15):
                    rotated_string_left = msg[i:] + msg[:i]
                    self.lcd.set_cursor_pos(1, 0)
                    self.lcd.print(rotated_string_left[:16])
                    await asyncio.sleep_ms(1000)
            else:
                self.lcd.print(msg)                
        
            await asyncio.sleep_ms(2000)

def remove_non_alpha(input_string):
    result_string = ""
    for char in input_string:
        if char.isalpha() or char == ' ':
            result_string += char
    return result_string

async def main():
    i2c = busio.I2C(scl = board.IO10, sda = board.IO11)
    morse = CodeLed(board.IO9, i2c)
    await asyncio.sleep_ms(1000)
    await morse.tx(code = "MORSE",msg = "SOS", t_ref = 300)
    await asyncio.sleep_ms(1000) 


if __name__ == "__main__":
    asyncio.run(main())