from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def abre_web():
    global chrome
    loop = True
    while loop == True:
        try:
            chrome_options = Options()
            chrome_options.add_argument('--user-data-dir=chrome-data')
            chrome = webdriver.Chrome(options=chrome_options)
            chrome.get('https://web.whatsapp.com/')
            loop = False
        except Exception as e:
            print('ERRO! NAVEGADOR JÁ ESTÁ EM USO!')
            print(e)
            input('PRESSIONE <ENTER> APÓS FECHAR OS NAVEGADORES')
    print('CONECTADO COM SUCESSO!')
    time.sleep(13) #Aumentar para conexões mais lentas
    print('Iniciando os trabalhos...')
    time.sleep(2)


def abre_contato(contato):
    div_class = '_2_1wd'
    div_xpath = '//div[@class="'+div_class+' copyable-text selectable-text' \
                '"][@contenteditable="true"][@data-tab="3"]'
    search_box = chrome.find_element_by_xpath(div_xpath)
    search_box.send_keys(contato)
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)
    print('Contato "{}" aberto!'.format(contato))
    time.sleep(3)


def envia_msg(mensagem):
    div_textbox = '_2A8P4'
    text_box = chrome.find_element_by_class_name(div_textbox)
    text_box.click()
    time.sleep(5)
    text_box.send_keys(mensagem + Keys.RETURN)


def acha_nao_lida():
    div_class = '_38M1B'
    nova_msg = chrome.find_element_by_class_name(div_class)
    nova_msg.click()


def lista_msg():
    div_class = '_3ExzF'
    post = chrome.find_elements_by_class_name(div_class)
    for item in post:
        try:
            mensagem = item.find_element_by_css_selector("span.selectable-text").text
            print(mensagem)
        except Exception as e:
            print('*** Mensagem sem Texto ***')


def le_ultima_msg():
    div_class = '_3ExzF'
    post = chrome.find_elements_by_class_name(div_class)
    ultimo = len(post) - 1
    texto = post[ultimo].find_element_by_css_selector("span.selectable-text").text
    return texto


def bot_hello():
    envia_msg('Olá, Eu sou o QBot! Muito Prazer!!!')
    time.sleep(2)
    envia_msg('Digite 1 para ver nosso Cardápio ou 2 para fazer seu pedido:')

def envia_cardapio():
    div_textbox = '_2A8P4'
    text_box = chrome.find_element_by_class_name(div_textbox)
    text_box.click()
    time.sleep(5)
    text_box.send_keys('NOSSO CARDÁPIO:' + Keys.SHIFT,Keys.RETURN,Keys.SHIFT)
    time.sleep(3)
    text_box.send_keys('X-Burguer  = R$ 15,00' + Keys.SHIFT,Keys.RETURN,Keys.SHIFT)
    time.sleep(3)
    text_box.send_keys('X-Salada   = R$ 18,00' + Keys.SHIFT,Keys.RETURN,Keys.SHIFT)
    time.sleep(3)
    text_box.send_keys('X-Tudo     = R$ 22,00' + Keys.SHIFT,Keys.RETURN,Keys.SHIFT)
    time.sleep(3)
    text_box.send_keys('Coca Lata  = R$  5,00' + Keys.RETURN)


def bot_mesmo_contato(contato):
    abre_contato(contato)
    time.sleep(5)
    envia_msg('Digite 1 para falar com nosso Bot ou 2 para aguardar atendimento humano!')
    time.sleep(15)
    while True:
        entrada = le_ultima_msg()
        if entrada == '1':
            bot_hello()
            time.sleep(15)
            while True:
                nova_msg = le_ultima_msg()
                if nova_msg == '1':
                    envia_cardapio()
                    time.sleep(20)
                    envia_msg('Digite 2 para fazer o seu pedido ou 3 para "deixar para outro dia". Nós entendemos!')
                elif nova_msg == '2':
                    envia_msg('Qual o seu pedido?')
                elif nova_msg == '3':
                    envia_msg('Agradecemos a preferência!')
                    break
                else:
                    pass
        elif entrada == '2':
            envia_msg('Aguarde um minuto... Um humano irá te atender...')
            pass
        else:
            pass

def bot_ouvindo():
    while True:
        tempo = 0
        try:
            acha_nao_lida()
            time.sleep(5)
            envia_msg('Digite 1 para falar com nosso Bot ou 2 para aguardar atendimento humano!')
            time.sleep(15)
            while tempo < 120:
                entrada = le_ultima_msg()
                if entrada == '1':
                    bot_hello()
                    time.sleep(15)
                    tempo = 0
                    while tempo < 120:
                        nova_msg = le_ultima_msg()
                        if nova_msg == '1':
                            envia_cardapio()
                            time.sleep(30)
                            envia_msg('Digite 2 para fazer o seu pedido ou 3 para "deixar para outro dia". Nós entendemos!')
                        elif nova_msg == '2':
                            envia_msg('Qual o seu pedido?')
                            time.sleep(30)
                            bot_ouvindo()
                        elif nova_msg == '3':
                            envia_msg('Agradecemos a preferência!')
                            bot_ouvindo()
                        else:
                            time.sleep(1)
                            tempo += 1
                            print(tempo)
                elif entrada == '2':
                    envia_msg('Aguarde um minuto... Um humano irá te atender...')
                    bot_ouvindo()
                else:
                    time.sleep(1)
                    tempo += 1
                    print(tempo)
        except:
            pass

abre_web()
bot_ouvindo()