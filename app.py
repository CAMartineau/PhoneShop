from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import getData, getProductData, getOrderLineProduct, addToOrderLine, deleteToOrderLine, connectDB
import mysql.connector
from mysql.connector import errorcode
#from passlib.hash import sha256_crypt
#from functools import wraps
#from forms import SignUpForm, LoginForm, PriceForm

application = Flask('glo2005_projet')

# cle géneré par os.urandom
#app.secret_key = b'{\xcd\xb6>\xf2\x02\xcc\x97\xefR\xae\xfflV\x172\x8bA\xf4e\x93\xd5p\xca'
#app.config['SESSION_TYPE'] = 'filesystem'



try:
  connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100',
                                database='phoneShop')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  connexion.close()	

@application.route('/')
def index():
    return render_template('index.html')



@application.route('/products', methods=['GET', 'POST'])
def products():
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
    # fetch les categories des produits
    query = 'SELECT * FROM Produits;'
    cursor = connexion.cursor(buffered=True)
    cursor.execute(query)
    cursor.close()
    data = cursor.fetchall()
    productsData = []
    for row in data:
            productsData.append({
                'idProduct': row[0],
                'prix': row[2],
                'name': row[1],
                'category': row[5],
                'image': row[3]
            })
    products = productsData
    # envoie la liste des categories a la page catogories.html
    return render_template('products.html', products=products)

	
application.run('0.0.0.0',8080)