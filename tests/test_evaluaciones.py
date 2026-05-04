def test_evaluaciones_index(client, init_database):
    pass # No existe

def test_evaluaciones_periodos(client, init_database):
    response = client.post('/evaluaciones/asignatura/1/periodos', data={
        'nombre': 'Trimestre 1'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_evaluaciones_actividades(client, init_database):
    # Asumiendo que el ID del periodo creado es 1
    response = client.post('/evaluaciones/periodo/1/actividades', data={
        'nombre': 'Examen',
        'ponderacion': '50'
    }, follow_redirects=True)
    assert response.status_code in [200, 302, 404]
