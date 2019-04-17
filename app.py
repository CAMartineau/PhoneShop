from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import getOneProduct
import mysql.connector
from mysql.connector import errorcode
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

application = Flask(__name__)

# cle géneré par os.urandom
application.secret_key = b'{\xcd\xb6>\xf2\x02\xcc\x97\xefR\xae\xfflV\x172\x8bA\xf4e\x93\xd5p\xca'
application.config['SESSION_TYPE'] = 'filesystem'



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


def checkLoginForAccess(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'session_on' in session and session['session_on']:
            return f(*args, **kwargs)
        else:
            flash("Veuillez d'abord vous connecter", 'danger')
            return redirect('/inscription')

    return wrap


class searchForm(Form):
    model = StringField([validators.Length(min=1, max=50)])

@application.route('/products', methods=['GET', 'POST'])
def products():
    
    form = searchForm(request.form)
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
	
    if request.method == 'POST':
	    form = searchForm(request.form)
	    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
	    query = 'SELECT * FROM Produits WHERE model LIKE (%s);'
	    cursor = connexion.cursor(buffered=True)
	    model = form.model.data
	    model += '%'
	    cursor.execute(query,(model,))
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
	    return render_template('products.html',products=products, form=form)		
    return render_template('products.html', products=products, form=form)

@application.route('/products/search', methods=['GET', 'POST'])
def search():
	    form = searchForm(request.form)
	    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
	    query = 'SELECT * FROM Produits WHERE model LIKE (%s) ;'
	    cursor = connexion.cursor(buffered=True)
	    model = form.model.data
	    cursor.execute(query,(model,))
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
	    return render_template('products.html',products=products, form=form)	

def addToCart(id_user, id_produit, quantity, unitPrice):
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
    cur = connexion.cursor(buffered=True)
    cur.execute("SELECT * FROM phoneShop.Pannier WHERE id_user = %s AND id_Produit = %s", [str(id_user), str(id_produit)])
    if cur.rowcount == 0:
        cur.execute("INSERT INTO phoneShop.Pannier (id_user, id_produit, quantity, unitPrice) VALUES ( %s, %s, %s, %s);",[str(id_user), str(id_produit), str(quantity), str(unitPrice)])
        connexion.commit()
        return True
    else:
        return False
    cur.close()
    connexion.close()
	
@application.route('/products/<string:id>/', methods=['GET', 'POST'])
@checkLoginForAccess
def product(id):


    if request.method == 'POST':
	
        product2 = getOneProduct(id)
        price = product2.get('prix')
        boolAddedToCart = addToCart(session['idUser'], id, request.form['quantity'], price)
        if (boolAddedToCart):
            flash('Produit ajouter à votre panier', category='info')
            return redirect('/products/' + str(id) + '/')
        else:
            flash('Le produit est déjà présent dans votre panier', category='warning')
            return redirect('/products/' + str(id) + '/')

    return render_template('product.html', product=getOneProduct(id), userId=session['idUser'])

	
class InscriptionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    password = PasswordField('Mot de passe',
                             [validators.Required(),validators.EqualTo('passwordConfirm', message='Passwords must match')])
    
    passwordConfirm = PasswordField('Confirmer le mot de passe')

@application.route('/inscription', methods=['GET', 'POST'])
def inscription():



    form = InscriptionForm(request.form)
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')

    cursor = connexion.cursor(buffered=True)
    #form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        lastname = form.lastname.data
        password = sha256_crypt.encrypt(str(form.password.data))		
	  
        query = "INSERT INTO Users ( email, prenom, nom, motDepass) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email,name,lastname,password))
        connexion.commit()
        cursor.close()
        
        userId = cursor.lastrowid
        cursor.close()
        flash("Votre nouveau compte est inscris", category='success')

        session['idUser'] = userId
        session['session_on'] = True
        session['email'] = email
        session['name'] = name
        return redirect('/')

    return render_template('inscription.html', form=form)

class LoginForm(Form):
    # les 2 champs sont obligatoires
    email = StringField('Adresse courriel', [validators.data_required(message='Ce champ doit etre remplis')])
    password = PasswordField('Mot de passe', [validators.data_required(message='Ce champ doit etre remplis')])


@application.route('/connection', methods=['GET', 'POST'])
def connection():
    
	
    form = LoginForm(request.form)
	
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100',database='phoneShop')	
	
    cursor = connexion.cursor(buffered=True)

    if request.method == 'POST':

        email = form.email.data

        query = "SELECT COUNT(*) FROM Users WHERE email LIKE (%s)"
        cursor.execute(query,(email,))
        connexion.commit()
        response = cursor.fetchone()
        count = response[0]
        # si le email n'existe pas, la reponse est vide
        if count == 0:
            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
            cursor.close()
            return render_template('index.html')
        else:
			
            cursor.close()
            cursor = connexion.cursor(buffered=True)
            query2 = "SELECT * FROM Users WHERE email LIKE (%s)"
            cursor.execute(query2,(email,))
            connexion.commit()
            response1 = cursor.fetchall()
            for row in response1:
                        hashedpwd = row[4]
                        userId = row[0]
                        password = form.password.data

            # verifie que le mot de passe correspond au hash stocké dans la base de données
                        if sha256_crypt.verify(password, hashedpwd):
                            flash('Vous etes connecté', category='success')
                            session['session_on'] = True
                            session['email'] = email
                            session['idUser'] = userId
                            cursor.close()
                            return redirect('/')

            # cas ou le mot de passe est faux
                        else:
                            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
                            cursor.close()
                            return render_template('connection.html', form=form)

    return render_template('connection.html', form=form)

@application.route("/logout")
@checkLoginForAccess
def logout():
    session['session_on'] = False
    session['email'] = ''
    session['idUser'] = ''
    flash('Vous avez été deconnecté', category='success')
    return redirect('/')

	
def deleteToCart(idUser, idProduct):
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
    cur = connexion.cursor(buffered=True)
    cur.execute("SELECT * FROM phoneShop.Pannier WHERE id_user = %s AND id_produit = %s", [str(idUser), str(idProduct)])
    if cur.rowcount > 0:
        cur.execute("DELETE FROM phoneShop.Pannier WHERE id_user = %s AND id_produit = %s", [str(idUser), str(idProduct)])
        connexion.commit()
        return True
    else:
        return False
    cur.close()
    connexion.close()	
	

def getCartProduct(idUser):
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
    cur = connexion.cursor(buffered=True)
    cur.execute(
        "SELECT Produits.id_produit, Produits.model, Produits.price,Produits.imageUrl, Pannier.quantity FROM Produits INNER JOIN Pannier ON Produits.id_produit = Pannier.id_produit WHERE Pannier.id_user = (%s);",
        [str(idUser)])
    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'idProduct': row[0],
            'prix': row[2],
            'name': row[1],
            'image': row[3],
            'qty': row[4],
            'idUser': idUser
        })

    cur.close()
    connexion.close()

    return productsData	
	
@application.route("/panier", methods=['GET', 'POST'])
@checkLoginForAccess
def panier():
    if request.method == 'POST':
        boolIsInCart = deleteToCart(session['idUser'], int(request.form['idProduct']))
        if (boolIsInCart):
            flash('Produit retirer à votre panier', category='info')
            return redirect('/panier')
        else:
            flash("Le produit n'est pas présent dans votre panier", category='warning')
            return redirect('/panier')
    return render_template('panier.html',cartProduct=getCartProduct(session['idUser']))

	#cartProduct=getCartProduct(session['idUser']
application.run('0.0.0.0',8080)
if __name__ == '__main__':
    application.run(debug=True)