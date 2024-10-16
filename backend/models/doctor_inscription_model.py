import bcrypt
from bson import ObjectId
from itsdangerous import URLSafeTimedSerializer
from database import get_mysql_connection, get_mongo_connection  # Importer la connexion MySQL depuis ton fichier database.py


db = get_mongo_connection()

class DoctorModel:
    @staticmethod
    def register_doctor(doctor_data):
        connection = get_mysql_connection()  # Utilisation de la fonction de connexion MySQL
        try:
            cursor = connection.cursor(dictionary=True)

            # Vérifier si l'email existe déjà
            sql = "SELECT * FROM doctor WHERE email = %s"
            cursor.execute(sql, (doctor_data['email'],))
            existing_user = cursor.fetchone()

            if existing_user:
                return {"message": "Cet email est déjà utilisé"}, 400

            # Hacher le mot de passe
            hashed_password = bcrypt.hashpw(doctor_data['password'].encode('utf-8'), bcrypt.gensalt())

            # Insérer les données du docteur dans MySQL
            sql = """
            INSERT INTO doctor (full_name, date_of_birth, address, phone_number, email, password, 
                speciality, license_number, work_institution, country, province, ville, verification_token)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                doctor_data['full_name'], 
                doctor_data['date_of_birth'], 
                doctor_data.get('address', ''), 
                doctor_data['phone_number'], 
                doctor_data['email'], 
                hashed_password, 
                doctor_data['speciality'], 
                doctor_data['license_number'], 
                doctor_data['work_institution'], 
                doctor_data['country'], 
                doctor_data['province'], 
                doctor_data['ville'], 
                DoctorModel.generate_verification_token(doctor_data['email'])
            ))

            connection.commit()
            doctor_id = cursor.lastrowid  # Récupérer l'ID du docteur nouvellement créé

            return {"message": "Inscription réussie", "doctor_id": doctor_id}, 201

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def generate_verification_token(email):
        serializer = URLSafeTimedSerializer('YourSecretKey')
        return serializer.dumps(email, salt='email-verification')

    @staticmethod
    def verify_email(token, expiration=86400):
        serializer = URLSafeTimedSerializer('YourSecretKey')
        try:
            email = serializer.loads(token, salt='email-verification', max_age=expiration)
            # Mettre à jour le statut du docteur dans MySQL
            connection = get_mysql_connection()
            try:
                cursor = connection.cursor()
                sql = "UPDATE doctor SET is_verified = TRUE WHERE email = %s"
                cursor.execute(sql, (email,))
                connection.commit()
            finally:
                cursor.close()
                connection.close()

            return email
        except Exception as e:
            return False
        

    # Nouvelle méthode find_by_email pour rechercher le docteur par email
    @staticmethod
    def find_by_email(email):
        connection = get_mysql_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT * FROM doctor WHERE email = %s"
            cursor.execute(sql, (email,))
            doctor = cursor.fetchone()
            return doctor
        finally:
            cursor.close()
            connection.close()



    @staticmethod
    def check_password(password, hashed_password):
        # Vérifier que le mot de passe correspond au mot de passe haché
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    


    @staticmethod
    def update_doctor(doctor_id, data):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key in data:
            if key == "password":  # Si le mot de passe doit être mis à jour
                hashed_password = bcrypt.hashpw(data[key].encode('utf-8'), bcrypt.gensalt())
                fields.append("password = %s")
                values.append(hashed_password)
            else:
                fields.append(f"{key} = %s")
                values.append(data[key])

        # Ajouter l'ID du docteur pour la condition WHERE
        values.append(doctor_id)
        fields_str = ", ".join(fields)

        # Créer la requête SQL
        query = f"UPDATE doctor SET {fields_str} WHERE id = %s"
        cursor.execute(query, values)

        # Commit des changements
        conn.commit()

        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()

        return updated
    


    @staticmethod
    def get_doctor_by_id(doctor_id):
        connection = get_mysql_connection()
        try:
            cursor = connection.cursor(dictionary=False)  # Utiliser False si tu veux obtenir une liste/tuple
            query = """
                SELECT id, full_name, date_of_birth, phone_number, email, address, 
                    password, speciality, license_number, work_institution, 
                    country, province, ville
                FROM doctor
                WHERE id = %s
            """
            cursor.execute(query, (doctor_id,))
            doctor = cursor.fetchone()
            return doctor
        finally:
            cursor.close()
            connection.close()

    
    @staticmethod
    def get_all_symptoms():
        symptoms_list = []

        # Récupérer tous les symptômes dans la collection patient_symptoms
        symptoms = db.patient_symptoms.find()

        for symptom in symptoms:
            symptom_data = {
                "_id": str(symptom['_id']),
                "patient_id": symptom['patient_id'],
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "doctor_response": symptom.get('doctor_response', {}),
                "files": [
                    {
                        "file_id": str(file["file_id"]),
                        "filename": file["filename"],
                        "metadata": file["metadata"],
                        "uploadDate": file["uploadDate"]
                    } for file in symptom.get("files", [])
                ]
            }
            
            # Requête pour récupérer les fichiers associés aux symptômes via GridFS
            symptom_id = ObjectId(symptom['_id'])
            files = db.fs.files.find({"metadata.symptom_id": symptom_id})

            for file in files:
                file_data = {
                    "filename": file['filename'],
                    "file_id": str(file['_id']),
                    "metadata": {
                        "patient_id": file['metadata']['patient_id'],
                        "symptom_id": str(file['metadata']['symptom_id'])
                    },
                    "uploadDate": file['uploadDate']
                }
                symptom_data['files'].append(file_data)

            symptoms_list.append(symptom_data)

        return symptoms_list
    


    # Récupérer tous les symptômes soumis par un patient depuis la base de données
    @staticmethod
    def get_symptoms_by_id(symptom_id):
        try:
            # Convertir l'ID du symptôme en ObjectId
            symptom_object_id = ObjectId(symptom_id)
        except Exception:
            return {"message": "Invalid symptom ID format"}

        # Chercher le symptôme correspondant à l'ID unique
        symptom = db.patient_symptoms.find_one({"_id": symptom_object_id})
        
        if symptom:
            symptom_data = {
                "_id": str(symptom['_id']),
                "patient_id": symptom['patient_id'],
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "doctor_response": symptom.get('doctor_response', {}),
                "files": [
                    {
                        "file_id": str(file["file_id"]),
                        "filename": file["filename"],
                        "metadata": file["metadata"],
                        "uploadDate": file["uploadDate"]
                    } for file in symptom.get("files", [])
                ]
            }

            return symptom_data
        else:
            return {"message": "Symptom not found"}



  