# Noun Check: https://inkforall.com/noun-checker
# Synonyms: https://www.thesaurus.com

import os
import discord
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def trans_en(mess_cont, driver):
  driver.get(f"https://translate.google.com/?hl=vi&sl=auto&tl=en&text={mess_cont}&op=translate")
  time.sleep(4)
  return " ".join([i.text for i in driver.find_elements(By.CLASS_NAME, "JLqJ4b")])

def search(trans_en, driver):
  driver.get(f"https://www.google.com/search?q={trans_en}&aqs=chrome..69i57j69i60l2.5029j0j1&sourceid=chrome")
  time.sleep(10)
  all_link = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, "//a[@href]")]
  with open("links.txt", mode="w", encoding="utf8") as file:
    file.write("\n".join(all_link))
  return driver.find_element(By.CLASS_NAME, "lEBKkf").text
  
def trans_vi(eng, driver):
  driver.get(f'https://translate.google.com/?hl=vi&sl=en&tl=vi&text={eng.replace("&", "%26")}&op=translate')
  time.sleep(4)
  return " ".join([i.text for i in driver.find_elements(By.CLASS_NAME, "JLqJ4b")])


dis_rel = '''>>> `{0}`
-----------------
Kết quả tìm kiếm: {1}'''
dis_rel_en = '''```asciidoc
Anh hóa: {0} ({1})
-----------------
  + Kết quả tìm kiếm: {2}
  + Việt hóa: {3}
```'''

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global dis_rel, dis_rel_en
  if message.author == client.user:
    return

  if message.content.startswith("$!"):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    ser_st = " ".join([i for i in message.content[3:].split(" ") if not (i.startswith("[") and i.endswith("]"))])

    dis_rel_1 = search(ser_st, driver)
    dis_rel_2 = list(set(dis_rel_1.split(" ")))
    for i in dis_rel_2:
      if i in ser_st:
        dis_rel_1 = dis_rel_1.replace(i, f"__{i}__")
    dis_rel_3 = dis_rel.format(ser_st, dis_rel_1.replace("__ __", " "))
    if "[en]" in message.content[3:]:
      ser_txt = trans_en(ser_st, driver)
      relt_wrd = search(ser_txt, driver)
      dis_rel_3 += dis_rel_en.format(ser_txt, trans_vi(ser_txt, driver), relt_wrd, trans_vi(relt_wrd, driver))

    await message.channel.send(dis_rel_3)

client.run(os.environ['TOKEN'])
