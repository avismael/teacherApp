from flask import Blueprint, render_template
from models import Asignatura, Estudiante, Seccion

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    # Obtener conteos básicos
    total_asignaturas = Asignatura.query.count()
    total_estudiantes = Estudiante.query.count()
    total_secciones = Seccion.query.count()
    
    asignaturas = Asignatura.query.all()
    
    return render_template('dashboard.html', 
        total_asignaturas=total_asignaturas,
        total_estudiantes=total_estudiantes,
        total_secciones=total_secciones,
        asignaturas=asignaturas
    )
