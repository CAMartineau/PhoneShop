CREATE database phoneShop;
USE phoneShop;
CREATE TABLE IF NOT EXISTS Users(id_user INT NOT NULL AUTO_INCREMENT, email VARCHAR(50) not null, prenom VARCHAR(50) not null, nom VARCHAR(50) not null,    motDepass VARCHAR(50) NOT NULL, PRIMARY KEY (id_user));
CREATE TABLE IF NOT EXISTS Suppliers (id_suppliers INT NOT NULL AUTO_INCREMENT, name VARCHAR(50), description VARCHAR(50), PRIMARY KEY (id_suppliers));
CREATE TABLE Produits(id_produit INT NOT NULL AUTO_INCREMENT,model VARCHAR(50), price DECIMAL(10,2), imageUrl VARCHAR(500), memory VARCHAR(50), display_size VARCHAR(50), weight VARCHAR(50), bluetooth VARCHAR(50), cpu VARCHAR(50), headphone_jack INT(1), id_suppliers INT, PRIMARY KEY(id_produit), FOREIGN KEY (id_suppliers) REFERENCES Suppliers(id_suppliers));
CREATE TABLE IF NOT EXISTS Orders(id_order INT(20), id_user INT(5), orderedDate Date, orderStatus VARCHAR(20), shipToAdress VARCHAR(20), shipToCity VARCHAR(20), shipToCountry VARCHAR(20), shipToPostalCode VARCHAR(20), PRIMARY KEY (ID_Order), FOREIGN KEY (ID_User) REFERENCES Users(ID_User));
CREATE TABLE IF NOT EXISTS  OrderLine(id_order INT(20), id_produit INT(20), quantity INT, unitPrice INT, lineNumber INT, PRIMARY KEY (id_order, id_produit), FOREIGN KEY (id_order) REFERENCES Orders(id_order), FOREIGN KEY (id_produit) REFERENCES Produits(id_produit));
CREATE INDEX modelIndex USING HASH ON Produits (model);
CREATE INDEX priceIndex USING BTREE ON Produits (price);
CREATE UNIQUE INDEX loginIndex USING HASH ON Users (email);


