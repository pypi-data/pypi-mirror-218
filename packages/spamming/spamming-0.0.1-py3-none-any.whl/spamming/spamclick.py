import pyautogui as pgi
from sys import argv as args

try:
  from winsound import Beep as b
  can_beep = True
except:
  can_beep = False

def main(clicks: int):
  """
  clicks: the number of times you want to click
  """

  print("STARTING IN 5 SECONDS")

  pgi.sleep(5)

  if can_beep:
    b(660, 500)

  for i in range(0, clicks):
    pgi.leftClick(interval=0.01)