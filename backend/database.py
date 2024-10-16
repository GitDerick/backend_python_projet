import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import gridfs

# Connexion à MySQL
def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="patients_infos",
            port=3306
        )
        if conn.is_connected():
            print("Connexion réussie à la base de données MySQL")
        return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None


def get_mongo_connection():
    # Remplace localhost et le port si ton instance MongoDB est sur un autre hôte ou port
    client = MongoClient('mongodb://localhost:27017/')
    
    # Connexion à la base de données "Projet_stage"
    db = client['Projet_stage']
    
    # Retourne la base de données pour interagir avec elle
    return db


def get_gridfs_connection():
    db = get_mongo_connection()  # Obtenir la connexion MongoDB
    fs = gridfs.GridFS(db)  # Initialisation de GridFS
    return fs