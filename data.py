import mysql.connector
# Cette methode permet de se connecter a la base de donnee
def connectDB():

	connexion = mysql.connector.connect(user='root',password='example',host='mysql', database='phoneShop')
	
	return connexion

# Cette methode permet d`aller chercher les informations d`un produit en particulier dans la table Products
def getOneProduct(id):
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
	    'model': data[1],
	    'id_suppliers': data[10]}
		
    cursor.close()
    connexion.close()
    return productsData

