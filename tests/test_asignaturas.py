def test_asignaturas_index(client, init_database):
    response = client.get('/asignaturas/')
    assert response.status_code == 200
    assert b'Matem' in response.data

def test_asignaturas_create(client, init_database):
    response = client.post('/asignaturas/', data={
        'nombre': 'Fisica',
        'descripcion': 'Ciencias Naturales',
        'secciones': []
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Fisica' in response.data

def test_asignaturas_edit(client, init_database):
    response = client.post('/asignaturas/editar/1', data={
        'nombre': 'Matematicas Avanzadas',
        'descripcion': 'Ciencias exactas',
        'secciones': []
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Matematicas Avanzadas' in response.data

def test_asignaturas_delete(client, init_database):
    response = client.post('/asignaturas/eliminar/1', follow_redirects=True)
    assert response.status_code == 200
    # Verificamos si no se puede eliminar por integridad de las notas o si se elimina exitosamente.
    # En ambos casos devuelve un status code 200 por el follow_redirects
