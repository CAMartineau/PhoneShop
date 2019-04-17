import mysql.connector
# Cette méthode permet de se connecter a la base de donnee
def connectDB():
	connexion = mysql.connector.connect(user='root',password='uTXukSvDgFXHTVzZ',host='mysql', database='phoneShop')
	
	return connexion
# Cette méthode vas chercher tous produits dans la base de donnée
def TousProduits(ModelInput,prixMin,prixMax):
	    connexion = connectDB()  
	    query = 'SELECT * FROM Produits WHERE modele LIKE (%s) AND prix BETWEEN (%s) AND (%s);'
	    cursor = connexion.cursor(buffered=True)
	    modele = ModelInput
	    modele += '%'
	    if prixMax == None: 
	        prixMax = 1500
	  
	    if prixMin == None: 
	        prixMin = 0
	    cursor.execute(query,(modele,prixMin,prixMax,))
	    cursor.close()
	    data = cursor.fetchall()
	    productsData = []
	    for row in data:
	        productsData.append({
				'idProduct': row[0],
				'prix': row[2],
				'name': row[1],
				'category': row[5],
				'image': row[3] })
	    products = productsData
	    return products
 
# Cette méthode permet d`aller chercher les informations d`un produit en particulier dans la table Products
def Produit(id):
    connexion = connectDB()
    
    query = "SELECT * FROM phoneShop.Produits WHERE id_produit = (%s);"
    # selection d'un produit selon son ID
    cursor = connexion.cursor(buffered=True)
    cursor.execute(query,(id,))
    data = cursor.fetchone()
	
    productsData = {
            'id_produit': id,
            'prix': data[2],
            'photo': data[3],
            'memory': data[4],
            'display_size': data[5],
            'weigth': data[6],
            'bluetooth': data[7],
	    'cpu': data[8],
	    'headphone_jack': data[9],
	    'modele': data[1],
	    'id_suppliers': data[10]}
		
    cursor.close()
    connexion.close()
    return productsData

# Cette méthode vérifie si un utilisateur existe déjà dans la base de donnée
def VerificationUserExistant(email):
	connexion = connectDB()
	query = "SELECT COUNT(*) FROM Utilisateurs WHERE email LIKE (%s)"
	cursor = connexion.cursor(buffered=True)
	cursor.execute(query,(email,))
	reponse = cursor.fetchone()
	connexion.commit()
	count = reponse[0]
	if count == 0:
		utilisateur = 0
		cursor.close()
		connexion.close()
	else:
		utilisateur = 1
		cursor.close()
		connexion.close()
	return utilisateur

# Cette méthode ajoute un utilisateur dans la base de donnée
def AjoutUser(email,name,lastname,password):
	connexion = connectDB()
	query = "INSERT INTO Utilisateurs ( email, prenom, nom, motDepass) VALUES (%s, %s, %s, %s)"
	cursor = connexion.cursor(buffered=True)
	cursor.execute(query,(email,name,lastname,password,))
	connexion.commit()
	cursor.close()
	connexion.close()

# Cette méthode vas chercher les informations d'un utilisateur dans la base de donnée
def InfoUser(email):
	connexion = connectDB()
	query = "SELECT * FROM Utilisateurs WHERE email LIKE (%s)"
	cursor = connexion.cursor(buffered=True)
	cursor.execute(query,(email,))
	connexion.commit()
	InformationUser = cursor.fetchall()
	cursor.close()
	connexion.close()
	return InformationUser

# Cette méthode ajoute dans le Paniers d'un utilisateur un produit
def AjoutPanier(id_user, id_produit, quantity, prix_unitaire):
    connexion = connectDB()
    cursor = connexion.cursor(buffered=True)
    cursor.execute("SELECT * FROM phoneShop.Paniers WHERE id_user = %s AND id_Produit = %s", [str(id_user), str(id_produit)])
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO phoneShop.Paniers (id_user, id_produit, quantite, prix_unitaire) VALUES ( %s, %s, %s, %s);",[str(id_user), str(id_produit), str(quantity), str(prix_unitaire)])
        connexion.commit()
        return True
    else:
        return False
    cursor.close()
    connexion.close()

# Cette méthode enlève un produit du Paniers d'un utilisateur
def EnleverPanier(id_user, id_Produit):
    connexion = connectDB()
    cursor = connexion.cursor(buffered=True)
    cursor.execute("SELECT * FROM phoneShop.Paniers WHERE id_user = %s AND id_produit = %s", [str(id_user), str(id_Produit)])
    if cursor.rowcount > 0:
        cursor.execute("DELETE FROM phoneShop.Paniers WHERE id_user = %s AND id_produit = %s", [str(id_user), str(id_Produit)])
        connexion.commit()
        return True
    else:
        return False
    cursor.close()
    connexion.close()	

# Cette méthode vas chercher les produits dans le Paniers de l'utilisateur qui sont contenue dans la base de donnée
def ProduitsPannier(idUser):
    connexion = connectDB()
    cursor = connexion.cursor(buffered=True)
    cursor.execute(
        "SELECT Produits.id_produit, Produits.modele, Produits.prix,Produits.imageUrl, Paniers.quantite FROM Produits INNER JOIN Paniers ON Produits.id_produit = Paniers.id_produit WHERE Paniers.id_user = (%s);", [str(idUser)])
    data = cursor.fetchall()
    productsData = []
    connexion.commit()
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
    cursor.close()
    connexion.close()
    return productsData	