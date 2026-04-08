from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Asignatura, Seccion
from extensions import db

asignaturas_bp = Blueprint('asignaturas', __name__)

@asignaturas_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descr = request.form.get('descripcion')
        if not nombre:
            flash('El nombre es requerido', 'error')
            return redirect(url_for('asignaturas.index'))
        
        nueva = Asignatura(nombre=nombre, descripcion=descr)
        db.session.add(nueva)
        db.session.commit()
        flash('Asignatura creada', 'success')
        return redirect(url_for('asignaturas.index'))
        
    asignaturas = Asignatura.query.all()
    return render_template('asignaturas/index.html', asignaturas=asignaturas)

@asignaturas_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    asignatura = Asignatura.query.get_or_404(id)
    secciones_disponibles = Seccion.query.all()
    return render_template('asignaturas/detalle.html', asignatura=asignatura, secciones_disponibles=secciones_disponibles)

@asignaturas_bp.route('/<int:asignatura_id>/matricular_seccion', methods=['POST'])
def matricular_seccion(asignatura_id):
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    seccion_id = request.form.get('seccion_id', type=int)
    if seccion_id:
        seccion = Seccion.query.get(seccion_id)
        if seccion and seccion not in asignatura.secciones:
            asignatura.secciones.append(seccion)
            db.session.commit()
            flash('Sección matriculada exitosamente en la asignatura', 'success')
        else:
            flash('La sección no existe o ya está matriculada', 'error')
    return redirect(url_for('asignaturas.detalle', id=asignatura.id))
