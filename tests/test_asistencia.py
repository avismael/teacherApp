def test_asistencia_index(client, init_database):
    response = client.get('/asistencia/')
    assert response.status_code == 200

def test_asistencia_seleccionar(client, init_database):
    response = client.get('/asistencia/tomar/1')
    assert response.status_code == 200

def test_asistencia_registro(client, init_database):
    response = client.post('/asistencia/guardar', data={
        'seccion_id': '1',
        'fecha': '2026-05-01',
        'hora': '08:00',
        'turno': 'Matutino'
    })
    assert response.status_code in [200, 302]
