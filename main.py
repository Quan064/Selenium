# https://www.randomlists.com/websites?dup=false&qty=400

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def inp():
  inp_entered = False
  while not inp_entered:
    with open("wait_for_confirmation.txt", encoding="utf8") as file:
      result = file.read()
    if result.rstrip(" ").endswith("."):
      inp_entered = True
  result_1 = result.split("\n\n")[0]
  result_2 = result.split("\n\n")[1][:-1].split("\n")
  result_2 = [i.split(":") for i in result_2]
  return result_2, result_1


def edit(inp, inp_2):
  with open("brain.txt", encoding="utf8") as file:
    bresult = [i.strip("\n") for i in file.readlines()]

  sof_ratio = []
  vt_ = inp_2.split(" ")
  print(inp)
    
  for i in inp:
    if i[0].startswith("DT(HĐ)") and not (i[0].endswith("ha") or i[0].endswith("w")):
      bresult_require = {j.split(": ")[0]:j.split(": ")[1] for j in bresult if j.startswith(f"    {i[0]}\\")}
      if not "" in bresult_require.values():
        for j in range(len(vt_)):
          rep = False
          try:
            ratio = [i.split(",") for i in bresult_require[f"{i[0]}\\vt_"].split(",,,")[j].split(",,")]
            for k in ratio:
              if k[0] == vt_[j]:
                k[1] = f"{(int(k[1])+1)/101*100:.2f}"
                rep = True
              else:
                k[1] = f"{(int(k[1]))/101*100:.2f}"
            if not rep:
              ratio += [ [vt_[j], "100"] ]
          except:
            ratio = [ [vt_[j], "100"] ]
          sof_ratio += [ratio]
      else:
        sof_ratio = [[ [i, "100"] ] for i in vt_]
      for j in range(len(sof_ratio)):
        for k in range(len(sof_ratio[j])):
          sof_ratio[j][k] = ",".join(sof_ratio[j][k])
        else:
          sof_ratio[j] = ",,".join(sof_ratio[j])
      vt_ = ",,,".join(sof_ratio)
      in_ = i[1]
      tr_ = inp_2.partition(in_)[0].strip().split(" ")[-1]
      sa_ = inp_2.partition(in_)[2].strip().split(" ")[0]
      def compute(tr_sa, trsa):
        if not "" in bresult_require.values():
          ratio = [i.split(",") for i in bresult_require[f"{i[0]}\\{trsa}"].split(",,")]
          # ratio = [ ["abc", "100"], ["def", "99"], ["ghi", "100"] ]
          # tr_ = "abc"
          rep = False
          for j in ratio:
            if j[0] == tr_sa:
              j[1] = f"{(int(j[1])+1)/101*100:.2f}"
              rep = True
            else:
              j[1] = f"{(int(j[1]))/101*100:.2f}"
          if not rep:
            ratio += [ [tr_sa, "100"] ]
        else:
          ratio = [ [tr_sa, "100"] ]
        for j in range(len(ratio)):
          ratio[j] = ",".join(ratio[j])
        return ",,".join(ratio)
      tr_ = compute(tr_, "tr")
      sa_ = compute(sa_, "sa")

      for j in range(len(bresult)):
        if bresult[j].startswith(f"    {i[0]}\\"):
          bresult[j] = f"    {i[0]}\\vt: {vt_}"
          bresult[j+1] = f"    {i[0]}\\in: {in_}"
          bresult[j+2] = f"    {i[0]}\\tr: {tr_}"
          bresult[j+3] = f"    {i[0]}\\sa: {sa_}"
          break

      with open("brain.txt", mode="w", encoding="utf8") as file:
        file.write("\n".join(bresult))
          
    elif i[0].startswith("SV"):
      pass
      
    else:
      pass

  
def test():
  a = [0, 1, 2, 3, 4]
  for i in range(len(a)):
    if a[i] == 2:
      a[i] = 3
  print(a)

def main():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  
  driver.get("https://vi.wikipedia.org/wiki/Special:Random")
  time.sleep(8)
  print(driver.current_url.replace(",","%2C").replace("(","%28").replace(")","%29"))
  
  all_texts = [i.text for i in driver.find_element(By.CLASS_NAME, "mw-parser-output").find_elements(By.TAG_NAME, "p")]
  sum = lambda lst: "" if not lst else lst[0] + sum(lst[1:])
  all_texts = sum(all_texts)
  try:
    all_texts += "\n" + driver.find_element(By.CLASS_NAME, "references").text
  except:
    pass
  all_texts += all_texts + "\n\n"
  
  with open("wait_for_confirmation.txt", mode="w", encoding="utf8") as file:
    file.write(all_texts)

if __name__ == "__main__":
  main()
  edit(*inp())
  # test()
