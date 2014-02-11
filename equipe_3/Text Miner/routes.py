from flask import Flask, render_template, request
from forms import SearchForm, AdvancedSearchForm
import manSearch, lucene

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/advancedSearch')
def advancedSearch():
  form = AdvancedSearchForm()
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('advancedSearch.html', form=form)
    else:   
      return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
  
  elif request.method == 'GET':
    return render_template('advancedSearch.html', form=form)   

@app.route('/', methods=['GET', 'POST'])
def search():
  form = SearchForm()
  
  if request.method == 'POST':
    if form.validate() == False:
      pol = manSearch.serarch      
      return render_template('search.html', form=form)
    else:   
      return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
  
  elif request.method == 'GET':
    return render_template('search.html', form=form)   

@app.route('/result', methods=['GET', 'POST'])
def result():
  try:
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
  except Exception, e:
    pass

  extras = dict(request.args)
  nome = extras.pop('nome')[0]
  politicos = manSearch.search(nome, **extras)

  return render_template('result.html', results=politicos)

@app.route('/pagina', methods=['GET', 'POST'])
def pagina():
  try:
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
  except Exception, e:
    pass

  extras = dict(request.args)
  nome = extras.pop('nome')[0]
  politicos = manSearch.search(nome, **extras)

  return render_template('page.html', results=politicos) 


if __name__ == '__main__':
  app.run(debug=True)
