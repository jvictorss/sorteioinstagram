from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random

app = Flask('Sorteio Instagram')

#setup para usar webdriver no repl.it
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#driver
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1024, 768)

winners = []
def sorteio(url_post):
  ## ABRE PAGINA LOGIN
  url_ig = 'https://www.instagram.com/'
  driver.get(url_ig)
  sleep(4)

  #### FAZ LOGIN
  ## seleciona elementos (inputs e botão)
  input_username = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
  input_password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
  btn_login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
  ## faz as ações
  input_username.send_keys('bushicoder') #inserir usuario
  input_password.send_keys('Iwilllearn') #inserir senha
  btn_login.click()
  sleep(5)

  try:
    btn_not_now = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
    if btn_not_now.is_displayed():
      btn_not_now.click()
      sleep(4)
  except:
    pass

  ### APÓS LOGIN ABRE O POST
  driver.get(url_post)
  sleep(4)

  print('Robos buscando os comentários... \n Aguarde...')

  sleep(2)

  ## tenta
  try:
    ## seleciona btn de carregar mais comentarios 
    btn_more_comments = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button')
    ## enquanto o btn existing (is diplayed)
    while btn_more_comments.is_displayed():
      #clique nele
      btn_more_comments.click()
      sleep(4)
      #seleciona ele denovo
      btn_more_comments = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button')
  #tratativa de erro quando o botao nao poder ser mais selecionado
  #ou não existe.
  #poderia deixar apenas o pass mas uso o print para tbm ver o erro ;) 
  except:
    pass
  sleep(3)

  ### PEGO TODOS COMENTARIOS
  comments = driver.find_elements_by_class_name('gElp9')

  ## loop pegando cada usuario
  for comment in comments:
    username = comment.find_element_by_class_name('_6lAjh').text
    #verifico se nao esta na lista já
    if username not in winners:
      #adiciono usuario na lista
      winners.append(username)

  #seleciono o vencedor
  winner = random.choice(winners)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/result')
def result():
  url = request.args.get('url')
  capture(url)
  num = request.args.get('winners')
  users = len(winners)
  
  
  if num == '1': 
    choice1 = random.choice(winners)
  elif num == '2':
    choice1 = random.sample(winners, 2)
  elif num == '3':
    choice1 = random.sample(winners, 3)

  return render_template('result.html', url=url, users=users, num=num, choice1=choice1)

app.run(host='0.0.0.0')
