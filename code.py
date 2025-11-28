import asyncio
import board
from codeled import CodeLed
import busio
import random

def pick_message():
    try:
        with open("messages.txt", "r") as f:
            messages = f.readlines()
            #print(messages)
            #message = messages[2]
            message = random.choice(messages)
            print("message chosen from filesystem")
    except OSError as e:
        print("Internal message")
        message = "Cuantos dejarian de ser esclavos por el precio de una bomba al mar."
    print(message)
    return message

async def main():
    morse = CodeLed(board.IO9, busio.I2C(scl = board.IO10, sda = board.IO11))
    await asyncio.sleep(1)
    morse.lcd.set_cursor_pos(0, 0)
    morse.lcd.print("Iniciar")
    await morse.restart_game()
    await asyncio.sleep(1)
    while True:
        picked_msg = pick_message()
        reset_protection = asyncio.create_task(morse.count_2_reset())
        await morse.tx(code = "MORSE",msg = picked_msg, t_ref = 500)
        reset_protection.cancel()
        await morse.show_msg()
        printing = asyncio.create_task(morse.print_msg(picked_msg))
        await morse.restart_game()
        printing.cancel()
        await asyncio.sleep(1)                

if __name__ == "__main__":
    asyncio.run(main())
