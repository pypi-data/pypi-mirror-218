from time import sleep
from sys import stdout

def test(x = None):
  y = "Тест пройден?"
  if x == y:
    x = "Пройден!"
    return x
  if x != None:
    return x
  else:
    x = "Тест успешно пройден!"
    return x

def loading(DELAY):
    JUMP_LEFT_SEQ = '\u001b[100D'
    for i in range(0, 101):
        sleep(DELAY)
        print(JUMP_LEFT_SEQ, end='')
        print(f'Progress: {i:0>3}%', end='')
        stdout.flush()
    return