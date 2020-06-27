from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


desktop = os.path.expanduser("~/Desktop")
pat = os.path.join(desktop, r"ArquivosPATH\chromedriver.exe")

arquivo = "minhalista.txt"
link1 = "https://www.linkedin.com/mynetwork/"
link2 = "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
login = ""
senha = ""

pessoas = 300
vezes = 3



def real():
    atingidos = []
    with open(arquivo, "r") as arq:
        linhas = arq.readlines()
        for linha in linhas:
            li = linha.split("\n")[0]
            atingidos.append(li)
    k = webdriver.Chrome(executable_path=pat)
    k.maximize_window()
    k.get(link2)
    time.sleep(2)
    bod = k.find_element_by_xpath("//input[@id='username']")
    bodi = k.find_element_by_xpath("//input[@id='password']")
    bod.send_keys(login)

    bodi.send_keys(senha)
    bodi.send_keys(Keys.ENTER)

    time.sleep(2)

    inp_xpath = "//a[@data-control-name='pymk_profile']"


    bod = k.find_element_by_xpath("//body")

    links = []
    print(f"Número de 'descidas': {int(pessoas / 3)}")
    for i in range(0, int(pessoas/10)):

        bod.send_keys(Keys.LEFT_CONTROL + Keys.END)
        time.sleep(1)

    nam = k.find_elements_by_xpath(inp_xpath)
    print(f"numero de resultados: {len(nam)}")
    for pess in nam:
        if pess.get_attribute("href") not in atingidos:
            links.append(pess.get_attribute("href"))
    print(f"Número de resultados para pesquisa: {len(links)}")
    # links.clear()
    # links.append("https://www.linkedin.com/in/jair-prado-03787343/")
    with open(arquivo, "a") as alvos:
        for pess in links[0:pessoas]:

            k.execute_script("window.open('');")
            k.switch_to.window(k.window_handles[1])
            k.get(pess)
            print(links.index(pess))
            time.sleep(2)
            bodi = k.find_element_by_xpath("//body")

            for i in range(0,3):
                bodi.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)

            k.close()


            k.switch_to.window(k.window_handles[0])



            alvos.write(pess + "\n")
    k.quit()

i = 0
while i != vezes:
    real()
    i +=1