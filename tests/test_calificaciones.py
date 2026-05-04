def test_calificaciones_seleccionar(client, init_database):
    pass # No hay ruta de seleccionar

def test_calificaciones_grid(client, init_database):
    from models import Asignatura, Seccion
    asignatura = Asignatura.query.get(1)
    seccion = Seccion.query.get(1)
    asignatura.secciones.append(seccion)
    init_database.session.commit()
    
    response = client.get('/calificaciones/grid/1/1')
    assert response.status_code == 200
