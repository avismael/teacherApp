def test_asignatura_model(init_database):
    from models import Asignatura
    asignatura = Asignatura.query.first()
    assert asignatura.nombre == "Matemáticas"
    assert asignatura.descripcion == "Ciencias exactas"

def test_seccion_model(init_database):
    from models import Seccion
    seccion = Seccion.query.first()
    assert seccion.nombre == "A"

def test_estudiante_model(init_database):
    from models import Estudiante
    estudiante = Estudiante.query.first()
    assert estudiante.nie == "12345"
    assert estudiante.genero == "Masculino"
    assert estudiante.apellidos == "Perez"
    assert estudiante.nombres == "Juan"

def test_periodo_model(init_database):
    from models import Periodo, Asignatura
    asignatura = Asignatura.query.first()
    periodo = Periodo(nombre="Periodo 1", asignatura_id=asignatura.id)
    init_database.session.add(periodo)
    init_database.session.commit()
    
    assert periodo.id is not None
    assert periodo.nombre == "Periodo 1"
    assert periodo.asignatura.nombre == "Matemáticas"
