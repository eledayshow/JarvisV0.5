import os #pip install os-win
import random
import gtts #pip install gTTS
from playsound import playsound #pip install playsound
import time
from pynput import keyboard #pip install pynput
from tkinter import * 
import platform
if platform.system() == 'Windows':
  from win10toast import ToastNotifier #pip install win10toast


isStart = False
tm = time.localtime()
isPressed = False
flag = True
timer = 10000000
isSleep = False
nWork = 0
dAction = False
kFunc = False

# Функции
def event (vText, title = 'Джарвис', message = '', log = ''):
  # вызов сообщения
  if platform.system() == 'Linux':
    command = 'notify-send "' + title + '" "' + message + '" -i /home/leo/coding/python/Jarvis/JarvisV0.5/J.png'
    os.system(command)
  elif platform.system() == 'Windows':
    ToastNotifier().show_toast(title, message, icon_path=r'C:\Users\leo\JarvisV0.5\J.png', duration=3)

  #
  play(vText)
  if log != '':
    print('[log] ' + log)

def play (text):
  if quietMode != True:
    voice = gtts.gTTS(text, lang="ru")
    voice.save('speech.mp3')
    playsound('speech.mp3')
  else:
    print(text)

def let (number):
  word = 'секунд'
  if number > 120:
    number = number / 60
    word = 'минут'
    if number > 120:
      number = number / 60
      word = 'h'
  number = round(number, 1)
  if (number * 10) % 10 == 0:
    number = int(number)
  if word != 'h':
    if type(number) == float:
      output = str(number) + ' ' + word + 'ы'
    elif number % 100 == 11 or number % 100 == 12 or number % 100 == 13 or number % 100 == 14 or number % 100 == 15:
      output = str(number) + ' ' + word
    elif number % 10 == 1:
      output = str(number) + ' ' + word + 'у'
    elif number % 10 == 2 or number % 10 == 3 or number % 10 == 4:
      output = str(number) + ' ' + word + 'ы'
    else:
      output = str(number) + ' ' + word
  else:
    if type(number) == float:
      output = str(number) + ' часа'
    elif number % 100 == 11 or number % 100 == 12 or number % 100 == 13 or number % 100 == 14 or number % 100 == 15:
      output = str(number) + ' часов'
    elif number % 10 == 1:
      output = str(number) + ' час'
    elif number % 10 == 2 or number % 10 == 3 or number % 10 == 4:
      output = str(number) + ' часа'
    else:
      output = str(number) + ' часов'
  return output, number

def fTime (startTime, s):
  global nWork
  s += nWork
  if s >= 60:
    m = s // 60
    s = s % 60
    if m >= 60:
      h = m // 60
      m = m % 60
  try:
    hFinishTime = startTime.tm_hour + h
  except:
    hFinishTime = startTime.tm_hour
  try:
    mFinishTime = startTime.tm_min + m
  except:
    mFinishTime = startTime.tm_min
  sFinishTime = startTime.tm_sec + s
  if sFinishTime > 60:
    sFinishTime -= 60
    mFinishTime += 1
  if mFinishTime > 60:
    mFinishTime -= 60
    hFinishTime += 1
  return hFinishTime, mFinishTime, sFinishTime

def iTime (startTime, finishTime):
  h = finishTime.tm_hour - startTime.tm_hour
  if h < 0:
    h += 24
  m = finishTime.tm_min - startTime.tm_min
  if m < 0:
    m += 60
    h -= 1
  s = finishTime.tm_sec - startTime.tm_sec
  if s < 0:
    s += 60
    m -= 1
  return h, m, s

def on_press(key):
  if kFunc:
    if str(key) == 'Key.ctrl_r':
      global timer, isPressed
      timer = time.localtime().tm_sec
      # if timer > hold:
      #   timer -= 60
      isPressed = True
      slp()
    
def on_release(key):
  if kFunc:
    global isPressed, timer, hold, isStart
    now = time.localtime().tm_sec
    if now < timer:
      now += 60
    if str(key) == 'Key.ctrl_r' and now - timer > hold:
      isStart = False
    timer = 1000000
    isPressed = False
    # print(isPressed)
listener = keyboard.Listener(
  on_press=on_press,
  on_release=on_release)
listener.start()

def slp():
  global isSleep
  global startSleep
  if isSleep:
    isSleep = False
    now = time.localtime()
    h = iTime(startSleep, now)[0]
    m = iTime(startSleep, now)[1]
    s = iTime(startSleep, now)[2]
    print('[log] h = ' + str(h) + ', m = ' + str(m) + ', s = ' + str(s))
    s = h * 60 * 60 + m * 60 + s
    output = let(s)
    global nWork
    nWork += s
    event('опять работать. вы отдыхали ' + output[0], 'Джарвис', 'Работа возобновлена', 'Работа продолжена: ' + timeLine(now))
  else:
    startSleep = time.localtime()
    event('работа приостановлена', 'Джарвис', 'Вы приоcтановили время работы. Чтобы продолжить повторите действие (клавишу)', 'Работа приостановлена: ' + timeLine(startSleep))
    isSleep = True

def rest():
  global restStartTime
  restStartTime = time.localtime()
  print('[log] Вы ушли отдыхать: ' + timeLine(restStartTime))
  window.destroy()
  window2 = Tk()  
  window2.title("Джарвис")
  Label(window2, text = 'Готовы продолжить работу?').pack(side = TOP, padx=5, pady=5)
  Button(window2, text = 'Да', command=lambda: window2.destroy()).pack(side = BOTTOM, padx=10)
  window.mainloop()
  restTime = iTime(restStartTime, time.localtime())
  event('с возвращением! продалжаем работать.', 'Джарвис', 'Вы отдыхали ' + str(restTime[0]) + ' часов, ' + str(restTime[1]) + ' минут, ' + str(restTime[2]) + ' секунд')
   
def timeLine(time, sign = ':'):
  try:
    output = str(time.tm_hour) + sign + str(time.tm_min) + sign + str(time.tm_sec)
    return output
  except:
    print('[log] Ошибка перевода времени в строку')

def nClick():
  window.destroy()

def readStngsFile(fileName):
  output = {}
  try:
    file = open(fileName)
    for line in file:
      i = 0
      s = line[i]
      key = ''
      of = 0
      while s != ':':
        s = line[i]
        key += s
        i += 1
        if line[i] == ':':
          break
        of += 1
        if of >= 256:
          raise Exception('Строка повреждена')
      s = line[i]
      of = 0
      while s == ' ':
        s = line[i]
        i += 1
        if line[i] != ' ':
          break
        of += 1
        if of >= 256:
          raise Exception('Строка повреждена')
      i += 2
      val = ''
      s = line[i]
      of = 0
      while s != ';':
        s = line[i]
        val += s
        i += 1
        if line[i] == ';':
          break
        of += 1
        if of >= 256:
          raise Exception('Строка повреждена')
      if val.find(',') != -1:
        val = tuple(item for item in val.split(','))

      output[key] = val
      
  except Exception as err:
    print('\033[31m[log] Ошибка работы с файлом: ' + str(err) + '\033[37m')

  return output

def filling(fileName):
  global rec, recommendations, dl, quietMode, fastMode, hold
  inFile = readStngsFile(fileName)
  if inFile.get('rec') == 't':
    rec = True
  elif inFile.get('rec') == 'f':
    rec = False
  else:
    print('\033[31m[log] Ошибка работы с файлом\033[37m')
  recommendations = {
    'starting': inFile.get('starting'),
    'actions': inFile.get('actions')
  }
  dl = int(inFile.get('dl'))
  if inFile.get('quietMode') == 't':
    quietMode = True
  elif inFile.get('quietMode') == 'f':
    quietMode = False
  else:
    print('\033[31m[log] Ошибка работы с файлом\033[37m')
  if inFile.get('fastMode') == 't':
    fastMode = True
  elif inFile.get('fastMode') == 'f':
    fastMode = False
  else:
    print('\033[31m[log] Ошибка работы с файлом\033[37m')
  hold = float(inFile.get('hold'))
filling('stngs.txt')



while True:
  if not isSleep:
    if isStart == False:
      if fastMode != True:
        play('система готова работать')
        play('для запуска введите s и нажмите enter')

      ipt = input('Для старта работы напишите s (чтобы изменить время паузы введите его в секундах): ')
      if ipt == 's' or ipt == 'ы' or ipt == '':
        kFunc = True
        play('всё готово. хорошей работы!')
        isStart = True
        startTime = time.localtime()
        print('[log] Время запуска: ' + str(startTime.tm_hour) + ':' + str(startTime.tm_min) + ':' + str(startTime.tm_sec))
      else:
        global dl
        try:
          dl = int(ipt)
          event('время работы изменено', 'Джарвис', 'Теперь отдых будет предложен через ' + str(dl) + ' секунд', 'время работы изменилось')
        except Exception as e:
          play('хотите выйти?')
          if input('y/n: ') == 'y':
            exit()
    elif isStart == True:
      tm = time.localtime()
      if tm.tm_hour == fTime(startTime, dl)[0] and tm.tm_min == fTime(startTime, dl)[1] and tm.tm_sec == fTime(startTime, dl)[2]:
        output = 'вы работаете уже ' + let(float(dl))[0]
        num = let(float(dl))[1]
        if num * 10 % 10 != 0:
          voice = 'пора сделать перерыв'
        else:
          voice = 'пора сделать перерыв. ' + output
        event(voice, 'Джарвис', output, 'Предложен перерыв: ' + timeLine(time.localtime()))
        play('пойдёте отдыхать?')
        output = 'Совет: ' + recommendations['starting'][random.randint(0, len(recommendations['starting']) - 1)] + ' ' + recommendations['actions'][random.randint(0, len(recommendations['actions']) - 1)] + '?'
        window = Tk()  
        window.title("Джарвис")
        lbl = Label(window, text = 'Будете отдыхать?').pack(side=TOP, padx=5)
        Label(window, text = output).pack(side=TOP, padx=5)
        yBtn = Button(window, text = 'Да', command=rest).pack(side = LEFT, padx=10, pady=5)
        nBtn = Button(window, text = 'Нет', command=nClick).pack(side = RIGHT, padx=10, pady=5)
        play(output)
        window.mainloop()
        startTime = time.localtime()
