import asyncio
import board
from codeled import CodeLed
import busio

mensaje = "Cuantos dejarian de ser esclavos por el precio de una bomba al mar."

print(mensaje)

async def main():
    morse = CodeLed(board.IO9, busio.I2C(scl = board.IO10, sda = board.IO11))
    await morse.tx(code = "MORSE",msg = mensaje, t_ref = 200)

if __name__ == "__main__":
    asyncio.run(main())
