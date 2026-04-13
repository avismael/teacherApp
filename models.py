from extensions import db

inscripciones = db.Table('inscripciones',
    db.Column('estudiante_id', db.Integer, db.ForeignKey('estudiante.id', ondelete="CASCADE"), primary_key=True),
    db.Column('seccion_id', db.Integer, db.ForeignKey('seccion.id', ondelete="CASCADE"), primary_key=True)
)

asignaturas_secciones = db.Table('asignaturas_secciones',
    db.Column('asignatura_id', db.Integer, db.ForeignKey('asignatura.id', ondelete="CASCADE"), primary_key=True),
    db.Column('seccion_id', db.Integer, db.ForeignKey('seccion.id', ondelete="CASCADE"), primary_key=True)
)

class Asignatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    secciones = db.relationship('Seccion', secondary=asignaturas_secciones, lazy='subquery',
        backref=db.backref('asignaturas', lazy=True))
    periodos = db.relationship('Periodo', backref='asignatura', lazy=True, cascade="all, delete-orphan")

class Seccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    estudiantes = db.relationship('Estudiante', secondary=inscripciones, lazy='subquery',
        backref=db.backref('secciones', lazy=True))

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nie = db.Column(db.String(20), unique=True, nullable=False)
    genero = db.Column(db.String(20), nullable=False, server_default='No especificado')
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    
    notas = db.relationship('Nota', backref='estudiante', lazy=True, cascade="all, delete-orphan")

class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignatura.id', ondelete="CASCADE"), nullable=False)
    
    actividades = db.relationship('Actividad', backref='periodo', lazy=True, cascade="all, delete-orphan")

class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ponderacion = db.Column(db.Float, nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id', ondelete="CASCADE"), nullable=False)
    
    notas = db.relationship('Nota', backref='actividad', lazy=True, cascade="all, delete-orphan")
    criterios = db.relationship('RubricaCriterio', backref='actividad', lazy=True, cascade="all, delete-orphan")

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id', ondelete="CASCADE"), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id', ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('actividad_id', 'estudiante_id', name='_actividad_estudiante_uc'),)

class RubricaCriterio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id', ondelete="CASCADE"), nullable=False)
    
    niveles = db.relationship('RubricaNivel', backref='criterio', lazy=True, cascade="all, delete-orphan")

class RubricaNivel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    puntaje = db.Column(db.Float, nullable=False)
    criterio_id = db.Column(db.Integer, db.ForeignKey('rubrica_criterio.id', ondelete="CASCADE"), nullable=False)

class RubricaEvaluacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id', ondelete="CASCADE"), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id', ondelete="CASCADE"), nullable=False)
    criterio_id = db.Column(db.Integer, db.ForeignKey('rubrica_criterio.id', ondelete="CASCADE"), nullable=False)
    nivel_id = db.Column(db.Integer, db.ForeignKey('rubrica_nivel.id', ondelete="CASCADE"), nullable=False)

    __table_args__ = (db.UniqueConstraint('estudiante_id', 'criterio_id', name='_est_crit_rubrica_uc'),)

class NotaRecuperacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id', ondelete="CASCADE"), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id', ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('periodo_id', 'estudiante_id', name='_periodo_estudiante_recup_uc'),)

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seccion_id = db.Column(db.Integer, db.ForeignKey('seccion.id', ondelete="CASCADE"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    turno = db.Column(db.String(20), nullable=False) # Matutino, Vespertino
    
    detalles = db.relationship('AsistenciaDetalle', backref='cabecera', lazy=True, cascade="all, delete-orphan")
    seccion = db.relationship('Seccion', backref=db.backref('asistencias', lazy=True))

class AsistenciaDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asistencia_id = db.Column(db.Integer, db.ForeignKey('asistencia.id', ondelete="CASCADE"), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id', ondelete="CASCADE"), nullable=False)
    estado = db.Column(db.String(20), nullable=False) # Presente, Ausente, Permiso, Escape
    nota = db.Column(db.Text, nullable=True)
    archivo_justificacion = db.Column(db.String(255), nullable=True)
    
    estudiante = db.relationship('Estudiante', backref=db.backref('registros_asistencia', lazy=True))
