def test_reportes_index(client, init_database):
    response = client.get('/reportes/')
    assert response.status_code == 200

def test_reportes_cuadro_final(client, init_database):
    response = client.get('/reportes/asignatura/1/1')
    assert response.status_code == 200

def test_reportes_boleta(client, init_database):
    response = client.get('/reportes/estudiante/1')
    assert response.status_code == 200

def test_reportes_asistencia(client, init_database):
    response = client.get('/reportes/asistencia/seccion/1')
    assert response.status_code == 200
