import pytest
import os
from app import create_app
from extensions import db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER_ASISTENCIA = '/tmp/asistencia_test'
    SECRET_KEY = 'test_secret'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        from models import Asignatura, Seccion, Estudiante
        # Basic data setup for tests
        asignatura = Asignatura(nombre="Matemáticas", descripcion="Ciencias exactas")
        seccion = Seccion(nombre="A")
        estudiante = Estudiante(nie="12345", genero="Masculino", apellidos="Perez", nombres="Juan")
        
        db.session.add(asignatura)
        db.session.add(seccion)
        db.session.add(estudiante)
        db.session.commit()
        
        yield db
