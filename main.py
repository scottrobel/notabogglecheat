from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path # this will get you the path variable
import requests
import pdb
import requests
import json
import re
import time
import random
from PIL import Image
import csv
import pyautogui
from pytesseract import pytesseract
import pyscreenshot as ImageGrab
dict_words_file = open("dictionary.csv", "r")
dict_words_2d = csv.reader(dict_words_file, delimiter=" ")
dict_words = []
pyautogui.PAUSE = 0.02
for word in dict_words_2d:
  dict_words.append(word[0])
session = requests.session()
session.get("https://www.dcode.fr/boggle-solver-any-size")
def get_tile_combos(letter_array):
  letters = json.dumps(letter_array)
  headers = {
      'authority': 'www.dcode.fr',
      'accept': 'application/json, text/javascript, */*; q=0.01',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      # 'cookie': 'PHPSESSID=337f378aff97532a5408085825f8d8cd; _ga=GA1.2.1182718030.1675018414; _gid=GA1.2.1148714636.1675018414; session_id=97474157-f8bb-4cf1-8879-e266a7871b11; __qca=P0-1657807918-1675018414101; __gpi=UID=00000998f52f8b1b:T=1675018414:RT=1675018414:S=ALNI_MabCZqJTmzUvOBrTVoPRBEwAk-SAw; cto_bundle=1CAz319zMlhlUzhIY2dwS0dVT0dyTnZYb29kTEFJZ2ZGWkpCZjhmZzJFdDFlakd6dnhqNXNaNDVtYWZPWTZXZmpOVFZsWmpNNnpxOXUwVmxPYkpweGVCY2ElMkZCUUFybzdrTG0wczJTQ0JPaEVWZzFvNWNxbGY5M0tobTJiT2JWejNSOUd1dk0lMkZzR0dxWHBnZEZZQXFCbVBONjd3JTNEJTNE; _gat_gtag_UA_647045_2=1; __gads=ID=95d5dff8369a9cd9-2243992f9eda007e:T=1675018414:S=ALNI_MY2dboGfQSwkv8SP6k6hPxbyy6vFw',
      'origin': 'https://www.dcode.fr',
      'referer': 'https://www.dcode.fr/boggle-solver-any-size',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest',
  }

  data = {
      'tool': 'boggle-solver-any-size',
      'boggle': '{"width":4,"height":4,"cells":' + letters + ',"headers":{"row":[null,null,null,null],"col":[null,null,null,null]}}',
      'min_length': '2',
      'max_length': '15',
      'dico': 'DICO_EN1',
      'no_diagonal': 'false',
      'straight': 'false',
      'connected_edges': 'false',
      'multiple_cell_use': 'false',
  }

  response = session.post('https://www.dcode.fr/api/', headers=headers, data=data)
  text_response = response.text
  groups = re.findall("('(?:#|b|g|l|\d|,)+')\)\.removeClass\('hover'\)",text_response)
  parsed_groups = []
  for group in groups:
    results = re.findall("(?:bgl(\d{1,2}),{0,1})+", group)
    word_letters = []
    for square in results:
      word_letter = letter_array[int(square)]
      word_letters.append(word_letter)
    word = "".join(word_letters).lower()
    if word in dict_words:
      parsed_groups.append(results)
  return parsed_groups
def click_canvas(x_offset, y_offset):
  el=driver.find_element_by_css_selector('canvas')
  action = webdriver.common.action_chains.ActionChains(driver)
  action.move_to_element_with_offset(el, x_offset, y_offset)
  action.click()
  action.perform()
def get_click_offset():
  return 0
def get_pause_time():
  return 0
# change ocr to get it in 2 rows
# change
def get_seleted_letters():
  time.sleep(0.4)
  try:
    screenshot = ImageGrab.grab()
  except:
    time.sleep(2)
    screenshot = ImageGrab.grab()
  croped_pic = screenshot.crop((1050, 710, 1270, 750))
  croped_pic.save("geeks.jpg")
  text = pytesseract.image_to_string(croped_pic).strip()
  raw_letters_reading = re.findall("((?:QU|[a-zA-Z]|\)))", text)
  letters = []
  for letter in raw_letters_reading:
    if letter == ")":
      # ) is read as J so I have to convert it manually
      letters.append("J")
    else:
      letters.append(letter)
  print("selected_letters: ", text)
  return letters
def get_board_state():
  rows = [[0,1,2,3, 7,6,5,4],[8,9,10,11,15,14,13,12]]
  in_order_letters = []
  for tile_numbers in rows:
    enter_word(tile_numbers)
    time.sleep(0.4)
    seletect_letters = get_seleted_letters()
    # try to get row one more time
    while(len(seletect_letters) != 8):
      enter_word(tile_numbers)
      time.sleep(0.3)
      seletect_letters = get_seleted_letters()
    if len(seletect_letters) == 8:
      first_row = seletect_letters[0:4]
      second_row = seletect_letters[4:]
      second_row.reverse()
      in_order_letters += first_row
      in_order_letters += second_row
  return in_order_letters
def move_to_tile(tile_number):
  tile_number = int(tile_number)
  if(tile_number == 0):
    x_offset = 1020 
    y_offset = 300
  if(tile_number == 1):
    x_offset = 1115
    y_offset = 300
  if(tile_number == 2):
    x_offset = 1210
    y_offset = 300
  if(tile_number == 3):
    x_offset = 1303
    y_offset = 300

  if(tile_number == 4):
    x_offset = 1020 
    y_offset = 390
  if(tile_number == 5):
    x_offset = 1115
    y_offset = 390
  if(tile_number == 6):
    x_offset = 1210
    y_offset = 390
  if(tile_number == 7):
    x_offset = 1303
    y_offset = 390

  if(tile_number == 8):
    x_offset = 1020
    y_offset = 488
  if(tile_number == 9):
    x_offset = 1115
    y_offset = 488
  if(tile_number == 10):
    x_offset = 1210
    y_offset = 488
  if(tile_number == 11):
    x_offset = 1303
    y_offset = 488

  if(tile_number == 12):
    x_offset = 1020
    y_offset = 590
  if(tile_number == 13):
    x_offset = 1115
    y_offset = 590
  if(tile_number == 14):
    x_offset = 1210
    y_offset = 590
  if(tile_number == 15):
    x_offset = 1303 # was 780
    y_offset = 590#was 400
  y_offset += 30
  pyautogui.moveTo(x_offset, y_offset)
def enter_word(tile_number_array):
  move_to_tile(tile_number_array[0])
  pyautogui.mouseDown()
  for tile_number in tile_number_array[0:]:
    move_to_tile(tile_number)
  pyautogui.mouseUp()
# DO NOT CHANGE THE WITHDR
def play_game():
  driver = webdriver.Chrome(executable_path="/home/scott/Downloads/chromedriver")
  driver.get("https://www.worldwinner.com/")
  user_name = "scottrobel"
  password = "ii27H@8y8yVeuUM"
  text_results = get_tile_combos("a t e a b a c e d m r i h e t a".split())
  if(len(text_results) == 0):
    print("cookie needs to be updated")
    pdb.set_trace()
  driver.set_window_position(30,0)
  driver.maximize_window()
  time.sleep(0.3)
  driver.execute_script('document.querySelector(\'[href="/cgi/login.html"]\').click()')
  user_name_field = driver.find_element_by_id('login-username')
  user_name_field.send_keys(user_name)
  password_field = driver.find_element_by_css_selector('[name="password"]')
  password_field.send_keys(password)
  time.sleep(0.3)
  driver.execute_script('document.querySelector(\'[type="submit"]\').click()')
  time.sleep(5)
  driver.get("https://www.worldwinner.com/cgi/tournament/list_single.pl?game_id=162")
  time.sleep(3)
  pdb.set_trace()
  # driver.execute_script('document.querySelector(\'[name="PlayButton167810_0"]\').click()')
  time.sleep(12)
  iframe = driver.find_element_by_css_selector('iframe')
  driver.switch_to.frame(iframe)
  pyautogui.moveTo(950, 580)
  pyautogui.click()
  time.sleep(7)
  for x in range(3):
    start_time = time.time()
    time_left = 60
    letter_array = get_board_state()
    combos = get_tile_combos(letter_array)
    for combo in combos:
      enter_word(combo)
      current_time = time.time()
      elapsed_time = current_time - start_time
      if elapsed_time > time_left:
        print("breaking the loop")
        break
    if elapsed_time < time_left:
      print("ran out of words. Waiting")
      time.sleep(time_left - elapsed_time + 0.5)
    time.sleep(4.5)
  time.sleep(5)
  pyautogui.moveTo(950, 670)
  pyautogui.click()
  time.sleep(6)
  driver.close()
# for x in range(11):
play_game()
# [490...870]
# adjust stopping time
# create fallback where it evaluates each letter individually