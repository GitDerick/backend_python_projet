# import mysql.connector
# from mysql.connector import Error
# from pymongo import MongoClient
# import gridfs

# # Connexion à MySQL
# def get_mysql_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="patients_infos",
#             port=3306
#         )
#         if conn.is_connected():
#             print("Connexion réussie à la base de données MySQL")
#         return conn
#     except Error as e:
#         print(f"Erreur lors de la connexion à MySQL: {e}")
#         return None


# def get_mongo_connection():
#     # Remplace localhost et le port si ton instance MongoDB est sur un autre hôte ou port
#     client = MongoClient('mongodb://localhost:27017/')
    
#     # Connexion à la base de données "Projet_stage"
#     db = client['Projet_stage']
    
#     # Retourne la base de données pour interagir avec elle
#     return db


# def get_gridfs_connection():
#     db = get_mongo_connection()  # Obtenir la connexion MongoDB
#     fs = gridfs.GridFS(db)  # Initialisation de GridFS
#     return fs



import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import gridfs

# Connexion à MySQL via le tunnel ngrok
def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="0.tcp.ngrok.io",  # URL ngrok pour MySQL
            user="root",  # Utilisateur MySQL
            password="",  # Mot de passe MySQL
            database="patients_infos",  # Nom de la base de données
            port=10232  # Port du tunnel ngrok pour MySQL
        )
        if conn.is_connected():
            print("Connexion réussie à la base de données MySQL via ngrok")
        return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL via ngrok: {e}")
        return None

# Connexion à MongoDB via le tunnel ngrok
def get_mongo_connection():
    try:
        # URL et port du tunnel ngrok pour MongoDB
        client = MongoClient('mongodb://2.tcp.ngrok.io:14889/')
        
        # Connexion à la base de données "Projet_stage"
        db = client['Projet_stage']
        
        print("Connexion réussie à MongoDB via ngrok")
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB via ngrok: {e}")
        return None

# Connexion à GridFS
def get_gridfs_connection():
    db = get_mongo_connection()  # Obtenir la connexion MongoDB via ngrok
    fs = gridfs.GridFS(db)  # Initialisation de GridFS
    return fs
