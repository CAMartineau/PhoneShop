from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import getData, getProductData, getOrderLineProduct, addToOrderLine, deleteToOrderLine, connectDB
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
            return redirect('/login')

    return wrap


def getProductData(id):
	
	connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')
    
	query = "SELECT * FROM phoneShop.Produits WHERE id_produit = (%s);"
    # selection d'un produit selon son ID
	cursor = connexion.cursor(buffered=True)
	cursor.execute(query,(id,))
	data = cursor.fetchone()
	
	productsData = {
            'idProduct': data[0],
            'prix': data[2],
            'photo': data[3],
            'memory': data[4],
            'display_size': data[5],
            'weigth': data[6],
            'bluetooth': data[7],
	    'cpu': data[8],
	    'headphone_jack': data[9],
	    'model': data[1],
	    'id_suppliers': data[10]}
		
	cursor.close()
	connexion.close()
	return productsData


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
	

    connection = connectDB()
    cur = connection.cursor()

    # selectionne tous les produits avec le model  spécifié
    cur.execute("SELECT * FROM phoneShop.Produits WHERE model LIKE (%s);", mymodel)

    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        # creation dun vecteur avec des tuples de produit
        productsData.append({
            'idProduct': row[0],
            'prix': row[2],
            'photo': row[3],
            'memory': row[4],
            'display_size': row[5],
            'weigth': row[6],
            'bluetooth': row[7],
	    'cpu': row[8],
	    'headphone_jack': row[9],
	    'model': row[1],
	    'id_suppliers': row[10]
        })

    cur.close()
    connection.close()
    return productsData


@application.route('/<string:id>/', methods=['GET', 'POST'])
@checkLoginForAccess
def product(id):


    if request.method == 'POST':
	
		
	
        boolAddedToCart = addToCart(session['idUser'], id, request.form['quantity'])
        if (boolAddedToCart):
            flash('Produit ajouter à votre panier', category='info')
            return redirect('/products/category/' + str(category) + '/' + str(id) + '/')
        else:
            flash('Le produit est déjà présent dans votre panier', category='warning')
            return redirect('/products/category/' + str(category) + '/' + str(id) + '/')

    return render_template('product.html', product=getProductData(id), userId=session['idUser'])

	
class InscriptionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    lastname = StringField('Lastname', [validators.Length(min=4, max=25)])
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    # mots de passe verifier par RegEx
    password = PasswordField('Mot de passe',
                             [validators.EqualTo('passwordConfirm', message='les mots de passes doivent correspondre'), validators.regexp(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", message='Le mot de passe doit contenir au moins 8 caracteres, 1 chiffre et une lettre')])
    
    passwordConfirm = PasswordField('Confirmer le mot de passe')

@application.route('/inscription', methods=['GET', 'POST'])
def inscription():



    form = InscriptionForm(request.form)
    connexion = mysql.connector.connect(user='root',password='example',host='192.168.99.100', database='phoneShop')

    cursor = connexion.cursor(buffered=True)
    #form = SignUpForm(request.form)
    if request.method == 'POST':
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
    flash('Vous avez été deconnecté', category='success')
    return redirect('/')

	
application.run('0.0.0.0',8080)
if __name__ == '__main__':
    application.run(debug=True)