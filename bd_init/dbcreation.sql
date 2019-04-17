CREATE database phoneShop;
USE phoneShop;
CREATE TABLE IF NOT EXISTS Utilisateurs(id_user INT UNSIGNED NOT NULL AUTO_INCREMENT, email VARCHAR(50) not null, prenom VARCHAR(50) not null, nom VARCHAR(50) not null,    motDepass VARCHAR(100) NOT NULL, PRIMARY KEY (id_user));

CREATE TABLE IF NOT EXISTS Marques (id_marque INT NOT NULL AUTO_INCREMENT, nom_marque VARCHAR(50), description_marque VARCHAR(50), PRIMARY KEY (id_marque));

CREATE TABLE Produits(id_produit INT UNSIGNED NOT NULL AUTO_INCREMENT, modele VARCHAR(50), prix DECIMAL(10,2), imageUrl VARCHAR(500), memoire VARCHAR(50), taille_ecran VARCHAR(50), poids VARCHAR(50), bluetooth VARCHAR(50), cpu VARCHAR(50), ecouteur INT(1), id_marque INT, PRIMARY KEY(id_produit), FOREIGN KEY (id_marque) REFERENCES Marques(id_marque));

CREATE TABLE IF NOT EXISTS Paniers(id_user INT UNSIGNED NOT NULL, id_produit INT UNSIGNED NOT NULL, quantite INT UNSIGNED NOT NULL,  prix_unitaire DECIMAL(10,2), PRIMARY KEY (id_user, id_produit), FOREIGN KEY (id_user) REFERENCES Utilisateurs(id_user) ON UPDATE CASCADE, FOREIGN KEY (id_produit) REFERENCES Produits(id_produit) ON UPDATE CASCADE);


CREATE INDEX modelIndex USING HASH ON Produits (modele);
CREATE INDEX priceIndex USING BTREE ON Produits (prix);
CREATE UNIQUE INDEX loginIndex USING HASH ON Utilisateurs (email);


