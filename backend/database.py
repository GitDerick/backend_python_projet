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


########################################


import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import gridfs

# Connexion à MySQL via le réseau privé interne de Railway
def get_mysql_connection():
    try:
        print("Tentative de connexion à MySQL sur Railway en réseau privé...")
        conn = mysql.connector.connect(
            host="mysql.railway.internal",  # Hostname interne privé Railway
            user="root",  # Nom d'utilisateur sur Railway
            password="XnaSAaGyjkiUWyWTgDubdJYosguSWEWN",  # Mot de passe Railway
            database="railway",  # Nom de la base de données sur Railway
            port=3306  # Port interne Railway (3306)
        )
        if conn.is_connected():
            print("Connexion réussie à la base de données MySQL sur Railway (réseau privé)")
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL via Railway: {e}")
        return None


# Connexion à MongoDB via le tunnel ngrok
def get_mongo_connection():
    try:
        print("Tentative de connexion à MongoDB via ngrok...")
        client = MongoClient('mongodb://2.tcp.ngrok.io:14889/')
        db = client['Projet_stage']
        print("Connexion réussie à MongoDB via ngrok")
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB via ngrok: {e}")
        return None

# Connexion à GridFS
def get_gridfs_connection():
    db = get_mongo_connection()  # Obtenir la connexion MongoDB via ngrok
    if db is not None:
        fs = gridfs.GridFS(db)  # Initialisation de GridFS
        return fs
    else:
        print("Impossible d'initialiser GridFS, connexion MongoDB échouée.")
        return None

# Test de la connexion MySQL sur Railway
if __name__ == "__main__":
    print("Test de connexion à MySQL sur Railway en réseau privé :")
    connection_railway = get_mysql_connection()
    if connection_railway:
        try:
            cursor = connection_railway.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Vous êtes connecté à la base de données:", record)
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête sur Railway: {e}")
        finally:
            cursor.close()
            connection_railway.close()
            print("Connexion MySQL Railway fermée.")
    else:
        print("Échec de la connexion à MySQL sur Railway (réseau privé).")

   









