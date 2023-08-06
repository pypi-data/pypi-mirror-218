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

def collatz(number):
    if number <= 0:
        print("Введите положительное число, отличное от нуля.")
        return
    
    count = 0
    while number != 1:
        print(number)
        if number % 2 == 0:
            print("Число", number, "четное")
            number = number // 2
        else:
            print("Число", number, "нечетное")
            number = (3 * number) + 1
        count += 1
    
    print(number)
    count += 1
    print("Количество операций:", count)