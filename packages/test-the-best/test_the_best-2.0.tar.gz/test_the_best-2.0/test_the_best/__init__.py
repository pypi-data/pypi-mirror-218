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