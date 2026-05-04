def test_secciones_index(client, init_database):
    response = client.get('/secciones/')
    assert response.status_code == 200

def test_secciones_create(client, init_database):
    response = client.post('/secciones/', data={
        'nombre': 'B'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_secciones_edit(client, init_database):
    response = client.post('/secciones/editar/1', data={
        'nombre': 'C'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_secciones_delete(client, init_database):
    response = client.post('/secciones/eliminar/1', follow_redirects=True)
    assert response.status_code == 200
