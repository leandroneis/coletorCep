from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from mysql.connector import errorcode
import time
import sys


def conexao():
    try:
        db_connection = mysql.connector.connect(host="localhost", user="seuusuariodobanco", passwd="suasenha", database="seudatabase")
        return db_connection
        print("Database connection made!")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)
    else:
        db_connection.close()

def configuracacaoDriver():
    firefoxOptions = Options()
    firefoxOptions.add_argument("-headless")
    driver = webdriver.Firefox(executable_path="./drivers/geckodriver", options=firefoxOptions)
    driver.maximize_window()
    return driver


def buscaElementosUrlGeral(url, codigoCep, codigo):
    try:
        db_connect = conexao()
        cursor = db_connect.cursor()
        driver = configuracacaoDriver()
        driver.get(url)
        time.sleep(1)

        botaoPesquisarCarregadoNaTela = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'btn_pesquisar')))
        if botaoPesquisarCarregadoNaTela.is_displayed():
            pesquisarCep = driver.find_element_by_xpath('//*[@id="endereco"]')
            time.sleep(0.5)
            pesquisarCep.send_keys(codigoCep)
            botaoBuscar = driver.find_element_by_xpath('//*[@id="btn_pesquisar"]')
            time.sleep(0.5)
            botaoBuscar.click()

        tabelaComInformacoes = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'resultado-DNEC')))

        if tabelaComInformacoes.is_displayed():
            mensagem = driver.find_element_by_xpath('//*[@id="mensagem-resultado"]')
            if mensagem.text == 'Não há dados a serem exibidos':
                return
            else:
                logradouro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr/td[1]')
                bairro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr/td[2]')
                localidadeuf = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr/td[3]')
                cep = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr/td[4]')

            localidade_uf = localidadeuf.text.split("/")
            print(
                f'Código -> {codigo} {logradouro.text}, {bairro.text}, {localidade_uf[0]}, {localidade_uf[1]} {cep.text}')
            sql = (
                "UPDATE cep SET logradouro= %s, bairro=%s, localidade=%s, uf=%s, cep=%s where codigo = %s")
            val = (logradouro.text, bairro.text, localidade_uf[0], localidade_uf[1], cep.text, codigo)
            cursor.execute(sql, val)
            db_connect.commit()
    except:
        pass
    finally:
        if driver is not None:
            driver.close()
            driver.quit()


def main(codigoInicial, codigoFinal):
    url = 'https://buscacepinter.correios.com.br/app/endereco/index.php?t'
    print("-:" * 20)
    print("Iniciando coleta dados CEP:")
    print(f"{url}")
    print("-:" * 20)

    db_connection = conexao()
    cursor = db_connection.cursor()

    sql = f"select codigo,cep from cep where codigo >= {codigoInicial} and codigo  <= {codigoFinal}"
    print(f"SQL:->{sql}")
    # sql = f"select codigo,cep from cep where codigo > 11999 and codigo  < 13000"
    cursor.execute(sql)

    for (codigo, cep) in cursor:
        buscaElementosUrlGeral(url, cep, codigo)

    cursor.close()
    db_connection.close()
    print("-" * 20)
    print(f"Cadastros faixa {codigoInicial} ate {codigoFinal} concluídos")
    print("Finished")
    print("-" * 20)


if __name__ == "__main__":
    codigoInicial = sys.argv[1]
    codigoFinal = sys.argv[2]
    main(codigoInicial, codigoFinal)