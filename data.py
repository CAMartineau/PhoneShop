import pymysql

# Cette methode permet de se connecter a la base de donnee
def connectDB():
    return pymysql.connect(host='localhost', user='root', password='UnAutreMotDePasse', db='phoneShop')

# Cette methode permet d`aller chercher les informations de tous les produits d`un model particulier dans la table Produits
def getData(mymodel):
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
            'prix': row[1],
            'photo': row[2],
            'memory': row[3],
            'display_size': row[4],
            'weigth': row[5],
            'bluetooth': row[6],
	    'cpu': row[7],
	    'headphone_jack': row[8],
	    'model': row[9],
	    'id_suppliers': row[10]
        })

    cur.close()
    connection.close()
    return productsData


# Cette methode permet d`aller chercher les informations d`un produit en particulier dans la table Products
def getProductData(id):
    connection = connectDB()
    cur = connection.cursor()

    # selection d'un produit selon son ID
    cur.execute("SELECT * FROM phoneShop.Produits WHERE id_produit =(%s);", id)

    data = cur.fetchone()

    # print(data)
    productsData = {
            'idProduct': row[0],
            'prix': row[1],
            'photo': row[2],
            'memory': row[3],
            'display_size': row[4],
            'weigth': row[5],
            'bluetooth': row[6],
	    'cpu': row[7],
	    'headphone_jack': row[8],
	    'model': row[9],
	    'id_suppliers': row[10]}

    cur.close()
    connection.close()
    return productsData

# Cette methode permet à un utilisateur de s'inscrire
def addUser(email, prenom, nom, motDepass):
	connection=connectDB()
	cur=connection.cursor()
	cur.execute(" SELECT MAX(id_user) FROM phoneShop.Users")
	idMax=cur.row[Max]
	idMax+=1
	cur.execute("INSERT INTO Users(id_user, email, prenom, nom, motDepass) VALUES (idMax, %s, %s, %s, %s);", 
	[str(email), str(prenom), str(nom), str(prenom), str(prenom), str(motDepass)])
	connection.commit()
	return True

# Cette methode permet  d'ajouter un article dans le panier d`achat de l`utilisateur
def addToOrderLine(idUser, idProduit, quantity):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute("SELECT * FROM phoneShop.OrderLine WHERE id_user = %s AND id_produit = %s", [str(idUser), str(idProduit)])
    if cur.rowcount == 0:
	#On recupère le prix total actuel et le nombre de produit contenu dans le panier
	totalprice=cur.row[totalPrice]
	totalquantity=cur.row[totalQuantity]
	#On recupère le prix unitaire du produit
	cur.execute("SELECT * FROM phoneShop.Produit WHERE id_produit = %s", [str(idUser)])
	unitprice=cur.row[price]
	#On mets à jour les nouvelles valeurs de totalPrice et totalQuantity dans la table OrderLine
	totalprice+=unitprice*quantity
	totalquantity+=quantity
       cur.execute("INSERT INTO phoneShop.OrderLine (id_user, id_produit, totalQuantity, totalPrice) VALUES ( %s, %s,totalquantity,totalprice);",
                    [str(idUser), str(idProduit)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

# Cette methode permet de retirer un produit contenu dans le panier d`achat de l`utilisateur
def deleteToOrderLine(idUser, idProduct):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute("SELECT * FROM phoneShop.OrderLine WHERE id_user = %s AND id_produit = %s", [str(idUser), str(idProduit)])
    if cur.rowcount > 0:
	#On recupère le prix total actuel et le nombre de produit contenu dans le panier
	totalprice=cur.row[totalPrice]
	totalquantity=cur.row[totalQuantity]
	#On recupère le prix unitaire du produit
	cur.execute("SELECT * FROM phoneShop.Produit WHERE id_produit = %s", [str(idUser)])
	unitprice=cur.row[price]
	#On mets à jour les nouvelles valeurs de totalPrice et totalQuantity dans la table OrderLine
	totalprice-=unitprice
	totalquantity-=1
        cur.execute("DELETE FROM phoneShop.OrderLine WHERE id_user = %s AND id_produit = %s", [str(idUser), str(idProduit)])
	cur.execute("UPDATE phoneShop.OrderLine SET totalQuantity=totalquantity, totalPrice=totalprice")
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

# Cette methode permet de chercher les produits dans le panier d`achat de l`utilisateur
# Pour cela, la methode effectue une jointure entre la table OrderLine et produits en fonction des id_produits dans le panier d`achat
def getOrderLineProduct(idUser):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute("SELECT Produits.id_produit, Produits.price, Produits.photo, Produits.memory, Produits.display_size, Produits.weigth, Produits.bluetooth, Produits.cpu, Produits.headphone_jack, Produits.model Orderline.totalQuantity FROM Produits INNER JOIN OrderLine ON Produits.id_produit = OrderLine.id_produit WHERE OrderLine.id_user = (%s);",
        idUser)
    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'id_produit': row[0],
            'prix': row[1],
            'photo': row[2],
            'memory': row[3],
            'display_size': row[4],
            'weigth': row[5],
            'bluetooth': row[6],
	    'cpu': row[7],
	    'headphone_jack': row[8],
	    'model': row[9]
	    'totalQuantity': row[10]
        })

    cur.close()
    connection.close()

    return productsData
