PhoneShop

# Aller dans Docker et dans le dossier qui contient l'application 

# Partir l'application ; 

docker-compose up

# Arreter l'application ;

docker-compose down 

# Delete l'application (Vous devez faire cela si vous changer app.py, requirements.txt) ; 

docker-compose down --rmi all


# L'application roule sur le port 5000 donc pour Linux : Localhost:5000 , pour Windows : IPDOCKER:5000