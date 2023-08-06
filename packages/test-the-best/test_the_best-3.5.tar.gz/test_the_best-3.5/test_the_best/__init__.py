from time import sleep
from sys import stdout

def test(x = None):
  JUMP_LEFT_SEQ = '\u001b[100D'
  DELAY = 0.05
  y = "Тест пройден?"
  if x == y:
    for i in range(0, 101):
      sleep(DELAY)
      print(JUMP_LEFT_SEQ, end='')
      print(f'Progress: {i:0>3}%', end='')
      stdout.flush()
    x = "Пройден!"
    return x
  if x != None:
    for i in range(0, 101):
      sleep(DELAY)
      print(JUMP_LEFT_SEQ, end='')
      print(f'Progress: {i:0>3}%', end='')
      stdout.flush()
    return x
  else:
    for i in range(0, 101):
      sleep(DELAY)
      print(JUMP_LEFT_SEQ, end='')
      print(f'Progress: {i:0>3}%', end='')
      stdout.flush()
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