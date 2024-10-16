import bcrypt
from database import get_mysql_connection
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_mongo_connection
from bson import ObjectId

db = get_mongo_connection()

class PatientModel:
    @staticmethod
    def create_patient(first_name, last_name, date_of_birth, phone_number, email, address, password):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO patients (first_name, last_name, date_of_birth, phone_number, email, address, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, date_of_birth, phone_number, email, address, password))
        patient_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return patient_id
    
    @staticmethod
    def update_patient(patient_id, data):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Générer dynamiquement la requête SQL en fonction des champs fournis
        fields = []
        values = []
        for key in data:
            # Si le mot de passe est présent, on le hache avant de le stocker
            if key == "password":
                #hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                hashed_password = bcrypt.hashpw(data[key].encode('utf-8'), bcrypt.gensalt())
                fields.append(f"{key} = %s")
                values.append(hashed_password)
            else:
                fields.append(f"{key} = %s")
                values.append(data[key])
        
        # Ajouter le patient_id à la fin pour la clause WHERE
        values.append(patient_id)
        fields_str = ", ".join(fields)

        query = f"UPDATE patients SET {fields_str} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated
    
    @staticmethod
    def delete_patient(patient_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "DELETE FROM patients WHERE id = %s"
        cursor.execute(query, (patient_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted


    @staticmethod
    def get_patient(patient_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM patients WHERE id = %s"
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        print(f"Patient data fetched from DB: {patient}")

        cursor.close()
        conn.close()
        return patient
    

    @staticmethod
    def get_patient_by_email(email):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM patients WHERE email = %s"
        cursor.execute(query, (email,))
        patient = cursor.fetchone()

        cursor.close()
        conn.close()
        return patient
    

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
    
    @staticmethod
    def get_medical_history(patient_id):
        medical_history = []

        # Récupérer tous les symptômes associés à ce patient
        symptoms = db.patient_symptoms.find({"patient_id": patient_id})

        for symptom in symptoms:
            symptom_data = {
                "_id": str(symptom['_id']),
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "files": []
            }

            # Récupérer les fichiers associés à ce symptôme
            files = db.fs.files.find({"metadata.symptom_id": ObjectId(symptom['_id'])})
            for file in files:
                file_data = {
                    "filename": file['filename'],
                    "file_id": str(file['_id']),
                    "uploadDate": file['uploadDate']
                }
                symptom_data['files'].append(file_data)

            medical_history.append(symptom_data)

        return medical_history
    

    # Récupérer tous les symptômes soumis par un patient depuis la base de données
    @staticmethod
    def get_symptoms_by_patient(patient_id):
        try:
            patient_id = int(patient_id)
        except ValueError:
            return []

        symptoms = db.patient_symptoms.find({"patient_id": patient_id})
        symptoms_list = []

        for symptom in symptoms:
            symptom_data = {
                "_id": str(symptom['_id']),  # Convertir ObjectId en chaîne
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "doctor_response": symptom.get('doctor_response', {}),
                "files": [
                    {
                        "file_id": str(file["file_id"]),  # Convertir ObjectId en chaîne
                        "filename": file["filename"],
                        "metadata": file["metadata"],
                        "uploadDate": file["uploadDate"]
                    } for file in symptom.get("files", [])
                ]
            }

            # Convertir symptom_id en ObjectId pour la requête dans GridFS
            symptom_id = ObjectId(symptom['_id'])

            files = db.fs.files.find({"metadata.symptom_id": symptom_id})

            for file in files:
                file_data = {
                    "filename": file['filename'],
                    "file_id": str(file['_id']),  # Convertir ObjectId en chaîne de caractères
                    "metadata": {
                        "patient_id": file['metadata']['patient_id'],
                        "symptom_id": str(file['metadata']['symptom_id'])  # Convertir ObjectId en chaîne de caractères
                    },
                    "uploadDate": file['uploadDate']
                }
                symptom_data['files'].append(file_data)

            symptoms_list.append(symptom_data)

        return symptoms_list