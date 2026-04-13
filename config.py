import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_muy_segura_para_el_sistema'
    
    # Ejemplo MySQL: mysql+pymysql://usuario:contraseña@localhost/nombre_bd
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'notas_v5.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Directorio para subidas de asistencia
    UPLOAD_FOLDER_ASISTENCIA = os.path.join(basedir, 'static', 'uploads', 'asistencia')
