def test_estudiantes_index(client, init_database):
    response = client.get('/estudiantes/')
    assert response.status_code == 200

def test_estudiantes_create(client, init_database):
    response = client.post('/estudiantes/', data={
        'nie': '67890',
        'apellidos': 'Gomez',
        'nombres': 'Maria',
        'genero': 'Femenino',
        'secciones': []
    }, follow_redirects=True)
    assert response.status_code == 200

def test_estudiantes_importar(client, init_database):
    pass # No testing file upload in this simple test
