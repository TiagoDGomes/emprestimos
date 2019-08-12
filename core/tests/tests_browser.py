from .base import TestCaseBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserBuscaTestCase(TestCaseBase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window() #For maximizing window
        self.addCleanup(self.browser.quit)
        super().setUp()

    def busca(self, texto):
        self.browser.get('http://localhost:8000/busca/')
        resposta = '---ERRO---'
        try:
            item_pesquisa = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.ID, "item_pesquisa"))
            )
            item_pesquisa.send_keys(texto)  
            WebDriverWait(self.browser,3).until(                
                EC.text_to_be_present_in_element((By.ID, 'tabela-resultado-corpo'), texto)
            )   
            resposta = self.browser.find_element_by_id('tabela-resultado-corpo').text
        except:
            pass        
        return resposta

    def test_pessoa_na_tabela(self):
        tabela_busca = self.busca(self.pessoa.nome)        
        self.assertIn(self.pessoa.nome, tabela_busca)

    def test_item_na_tabela(self):
        tabela_busca = self.busca(self.sala.nome)        
        self.assertIn(self.sala.nome, tabela_busca)
