from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from requete import getOneProduct, VerificationUserExistant, AjoutUser, InfoUser, EnleverPanier, ProduitsPannier, AjoutPanier
import mysql.connector
from formulaire import searchForm, InscriptionForm , ConnectionForm
from mysql.connector import errorcode
from passlib.hash import sha256_crypt
from functools import wraps

application = Flask(__name__)

# cle géneré par os.urandom
application.secret_key = b'{\xcd\xb6>\xf2\x02\xcc\x97\xefR\xae\xfflV\x172\x8bA\xf4e\x93\xd5p\xca'
application.config['SESSION_TYPE'] = 'filesystem'
 
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
	
@application.route('/products/<string:id>/', methods=['GET', 'POST'])
@checkLoginForAccess
def product(id):
    if request.method == 'POST':	
        product = getOneProduct(id)
        price = product.get('prix')
        boolAddedToCart = AjoutPanier(session['idUser'], id, request.form['quantity'], price)
        if (boolAddedToCart):
            flash('Produit ajouter à votre panier', category='info')
            return redirect('/products/' + str(id) + '/')
        else:
            flash('Le produit est déjà présent dans votre panier', category='warning')
            return redirect('/products/' + str(id) + '/')
    return render_template('product.html', product=getOneProduct(id), userId=session['idUser'])
	
@application.route('/inscription', methods=['GET', 'POST'])
def inscription():

    form = InscriptionForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        lastname = form.lastname.data
        password = sha256_crypt.encrypt(str(form.password.data))
        existe = VerificationUserExistant(email)
        if existe == 1:
            flash("Cette adresse courriel est déjà utilisé", category='warning')
            return render_template('inscription.html', form=form)
        else:
            AjoutUser(email,name,lastname,password)
            flash("Votre nouveau compte est inscris", category='success')      
            UserInfo = InfoUser(email)
            for row in UserInfo:
                        userId = row[0]
                        password = form.password.data
                        session['idUser'] = userId
                        session['session_on'] = True
                        session['email'] = email
                        session['name'] = name
                        return redirect('/')
    return render_template('inscription.html', form=form)

@application.route('/connection', methods=['GET', 'POST'])
def connection():
    
    form = ConnectionForm(request.form)
	
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100',database='phoneShop')	
	
    cursor = connexion.cursor(buffered=True)

    if request.method == 'POST':
        email = form.email.data
        existe = VerificationUserExistant(email)
        # si le email n'existe pas, la reponse est vide
        if existe == 0:
            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
            cursor.close()
            return render_template('connection.html', form=form)
        else:
			
            UserInfo = InfoUser(email)
            for row in UserInfo:
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
	
@application.route("/panier", methods=['GET', 'POST'])
@checkLoginForAccess
def panier():
    if request.method == 'POST':
        boolIsInCart = EnleverPanier(session['idUser'], int(request.form['idProduct']))
        if (boolIsInCart):
            flash('Produit retirer à votre panier', category='info')
            return redirect('/panier')
        else:
            flash("Le produit n'est pas présent dans votre panier", category='warning')
            return redirect('/panier')
    return render_template('panier.html',cartProduct=ProduitsPannier(session['idUser']))

application.run('0.0.0.0',8080)

if __name__ == '__main__':
    application.run(debug=True)