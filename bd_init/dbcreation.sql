CREATE database phoneShop;
USE phoneShop;
CREATE TABLE IF NOT EXISTS Users(id_user INT UNSIGNED NOT NULL AUTO_INCREMENT, email VARCHAR(50) not null, prenom VARCHAR(50) not null, nom VARCHAR(50) not null,    motDepass VARCHAR(100) NOT NULL, PRIMARY KEY (id_user));

CREATE TABLE IF NOT EXISTS Suppliers (id_suppliers INT NOT NULL AUTO_INCREMENT, name VARCHAR(50), description VARCHAR(50), PRIMARY KEY (id_suppliers));

CREATE TABLE Produits(id_produit INT UNSIGNED NOT NULL AUTO_INCREMENT,model VARCHAR(50), price DECIMAL(10,2), imageUrl VARCHAR(500), memory VARCHAR(50), display_size VARCHAR(50), weight VARCHAR(50), bluetooth VARCHAR(50), cpu VARCHAR(50), headphone_jack INT(1), id_suppliers INT, PRIMARY KEY(id_produit), FOREIGN KEY (id_suppliers) REFERENCES Suppliers(id_suppliers));

CREATE TABLE IF NOT EXISTS Pannier(id_user INT UNSIGNED NOT NULL, id_produit INT UNSIGNED NOT NULL, quantity INT UNSIGNED NOT NULL,  unitPrice DECIMAL(10,2), PRIMARY KEY (id_user, id_produit), FOREIGN KEY (id_user) REFERENCES Users(id_user) ON UPDATE CASCADE, FOREIGN KEY (id_produit) REFERENCES Produits(id_produit) ON UPDATE CASCADE);


CREATE INDEX modelIndex USING HASH ON Produits (model);
CREATE INDEX priceIndex USING BTREE ON Produits (price);
CREATE UNIQUE INDEX loginIndex USING HASH ON Users (email);


