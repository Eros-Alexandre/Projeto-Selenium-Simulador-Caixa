from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
import re
from datetime import date
from fpdf import FPDF


# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

path = r"C:\Users\USUARIO\pythonProject\dados.txt"
faixa = "PCVA UNID VINCULADA PF EMPREENDIMENTO COM FINANCIAMENTO PJ - (3048)"


def to_pdf(content, id, val):
    pdf = FPDF("P", "mm", "A4")
    pdf.set_font("helvetica", "", 8)
    pdf.add_page()
    for l in content:
        pdf.cell(200, 5, txt=l, ln=1, align="L")
    pdf.output(r"C:\Users\USUARIO\Desktop\SIMULAÇÕES\{}{}.pdf".format(id, val))


tipo_requisicao = input(
    "Digite 1 para realizar simulações com multiplas rendas e 2 com multiplos valores de imóveis:\n")


num_repeticao = 5
if tipo_requisicao == "1":
    valor_inicial_renda = int(input("O faixa de salário começa com qual valor?\n"))
    valor_final_renda = int(input("O faixa de salário termina com qual valor?\n"))
    intervalo_renda = int(input("Qual o intervalo?\n"))
    valor_do_imovel = input("Qual o valor do imóvel?\n")
    idade = int(input("Qual a idade do cliete?\n"))
    ctps = False
    intervalo = [x for x in range(valor_inicial_renda, valor_final_renda + intervalo_renda, intervalo_renda)]


    def calculateAge(age):
        today = date.today()
        nasc = date(today.year - age, today.month, today.day)
        return nasc.strftime("%d/%m/%Y")


    data_nascimento = calculateAge(idade)
    arquivo = 'tabela_simulacao_caixa.csv'

elif tipo_requisicao == "2":
    nome = input("Digite o nome do cliente:\n")
    valor_renda = int(input("Qual o valor da renda mensal do cliente?\n"))
    data_nascimento = input('Digite a data de nascimento no formato "00/00/0000":\n')
    intervalo = input("Digite os valores  dos imóveis:\n").split()
    dependentes = input("Possui dependentes ? Responda SIM ou NÃO:\n")
    dependentes.lower()
    ctps = input("O cliente tem 3 anos de CTPS assinada? Responda SIM ou NÃO:\n")
    ctps.lower()
    num_repeticao = 2
    intervalo_renda = 0

driver = webdriver.Chrome()
driver.get("https://www.portaldeempreendimentos.caixa.gov.br/simulador/")
driver.implicitly_wait(10)
driver.maximize_window()

for i in intervalo:

    for j in range(1, num_repeticao):
        # pag-1
        select = Select(driver.find_element_by_name('origemRecurso'))
        select.select_by_value('25')
        driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
        # pag-2
        select = Select(driver.find_element_by_id('categoriaImovel'))
        select.select_by_value('16')
        cidade = driver.find_element_by_id('cidade')
        cidade.send_keys('Rio De Janeiro - RJ')
        valor_imovel = driver.find_element_by_id('valorImovel')
        valor_imovel.clear()
        if tipo_requisicao == '1':
            valor_imovel.send_keys("{},00".format(valor_do_imovel))
            renda = driver.find_element_by_id('renda')
            renda.clear()
            renda.send_keys("{},00".format(i))
            if ctps == True:
                fator_redutor = driver.find_element_by_id('checkbox')
                fator_redutor.click()
            else:
                ctps = True
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-3
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-4
            nascimento = driver.find_element_by_id("dataNascimento")
            nascimento.send_keys(data_nascimento)
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-5
            element = driver.find_element(By.LINK_TEXT, faixa)
            driver.execute_script("arguments[0].click();", element)
            # pag-6
            select = Select(driver.find_element_by_id('rcrRge'))
            select.select_by_value('894')
            driver.find_element(By.ID, 'possuiMaisUmParticipante').click()
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()

            prazo = driver.find_element(By.ID, 'prazoObra')
            prazo.send_keys('36')
            driver.find_element(By.CSS_SELECTOR, '#cronogramaForm > div.form > fieldset > ul > li > a > span').click()
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a").click()
            texto = driver.find_element(By.ID, "main").text
            file = open(r'C:\Users\USUARIO\Desktop\SIMULAÇÕES\{}'.format(arquivo), 'a', encoding='utf-8', newline="")

            regex_data ='\d[0-9.,%]*'
            data = re.findall(regex_data, texto)
            new_data = [x.rstrip('\n') for x in data]
            w = csv.writer(file)
            w.writerow(new_data)
            file.close()
        else:
            valor_imovel.send_keys("{},00".format(i))
            renda = driver.find_element_by_id('renda')
            renda.clear()
            renda.send_keys("{},00".format(valor_renda))
            if ctps == "sim":
                fator_redutor = driver.find_element_by_id('checkbox')
                fator_redutor.click()
                ctps = False
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-3
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-4
            nascimento = driver.find_element_by_id('dataNascimento')
            nascimento.send_keys(data_nascimento)
            driver.find_element_by_css_selector("#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()
            # pag-5
            element = driver.find_element(By.LINK_TEXT, faixa)
            driver.execute_script("arguments[0].click();", element)
            # pag-61
            select = Select(driver.find_element_by_id('rcrRge'))
            select.select_by_value('894')
            if dependentes == "sim":
                driver.find_element(By.ID, 'possuiMaisUmParticipante').click()
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a > span").click()

            prazo = driver.find_element(By.ID, 'prazoObra')
            prazo.send_keys('36')
            driver.find_element(By.CSS_SELECTOR, '#cronogramaForm > div.form > fieldset > ul > li > a > span').click()
            driver.find_element(By.CSS_SELECTOR, "#bottom_bar > fieldset > ul > li:nth-child(2) > a").click()
            texto = driver.find_element(By.ID, "main").text
            f = open(r"dados.txt", "w+", encoding="latin-1", newline="\n")
            f.write(texto)
            f.seek(0)
            to_pdf(f, nome, "-{},00".format(i))
            # if os.path.exists(path):
            # os.remove(path)
        driver.get("https://www.portaldeempreendimentos.caixa.gov.br/simulador/")

driver.quit()
