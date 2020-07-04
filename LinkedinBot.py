from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


desktop = os.path.expanduser("~/Desktop")
pat = os.path.join(desktop, r"ArquivosPATH\chromedriver2.exe")

arquivo = "minhalista.txt"
link1 = "https://www.linkedin.com/mynetwork/"
link2 = "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fmynetwork%2F&fromSignIn=true&trk=cold_join_sign_in"
login = ""
senha = ""

pessoas = 280
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


    cont = 0
    links = []
    step = 10
    while True:
        cont += 1
        bod.send_keys(Keys.LEFT_CONTROL + Keys.END)
        time.sleep(1)
        if cont == 1 or cont%step == 0:
            links.clear()
            nam = k.find_elements_by_xpath(inp_xpath)
            for pess in nam:
                if pess.get_attribute("href") not in atingidos:
                    links.append(pess.get_attribute("href"))
            if len(links) >= pessoas:
                print("Step 1 complete")
                break


    # print(f"Número de 'descidas': {pessoas}")
    # for i in range(0, pessoas):
    #
    #     bod.send_keys(Keys.LEFT_CONTROL + Keys.END)
    #     time.sleep(1)
    #
    # nam = k.find_elements_by_xpath(inp_xpath)
    # print(f"numero de resultados: {len(nam)}")
    # for pess in nam:
    #     if pess.get_attribute("href") not in atingidos:
    #         links.append(pess.get_attribute("href"))
    # print(f"Número de resultados para pesquisa: {len(links)}")



    # links.clear()
    # links.append("https://www.linkedin.com/in/jair-prado-03787343/")
    with open(arquivo, "a") as alvos:
        for pess in links[0:pessoas]:

            k.execute_script("window.open('');")
            k.switch_to.window(k.window_handles[1])
            k.get(pess)

            try:
                bodi = k.find_element_by_xpath("//body")

            except:
                print(f"Stopped at {links.index(pess)}")
                break
            try:
                test = k.find_element_by_xpath("//a[@data-tracking-control-name='public_profile_nav-header-signin']")
                print(f"Stopped at {links.index(pess)}")
                break
            except:
                print(links.index(pess))


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