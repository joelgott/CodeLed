import asyncio
import board
from codeled import CodeLed
import busio
import random

try:
    with open("/messages.txt", "r") as f:
        messages = f.readlines()
        #print(messages)
        #message = messages[2]
        message = random.choice(messages)
        print("message chosen from filesystem")
except OSError as e:
    print("Internal message")
    message = "Cuantos dejarian de ser esclavos por el precio de una bomba al mar."

print(message)

async def main():
    morse = CodeLed(board.IO9, busio.I2C(scl = board.IO10, sda = board.IO11))
    await morse.tx(code = "MORSE",msg = message, t_ref = 200)

if __name__ == "__main__":
    asyncio.run(main())
