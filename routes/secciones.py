import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Seccion, Estudiante
from extensions import db

secciones_bp = Blueprint('secciones', __name__)

@secciones_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre de la sección es requerido', 'error')
            return redirect(url_for('secciones.index'))
            
        nueva = Seccion(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
        flash('Sección creada correctamente', 'success')
        return redirect(url_for('secciones.index'))
        
    secciones = Seccion.query.all()
    return render_template('secciones/index.html', secciones=secciones)

@secciones_bp.route('/<int:id>', methods=['GET'])
def detalle(id):
    seccion = Seccion.query.get_or_404(id)
    estudiantes_totales = Estudiante.query.order_by(Estudiante.apellidos).all()
    return render_template('secciones/detalle.html', seccion=seccion, estudiantes_totales=estudiantes_totales)

@secciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    seccion = Seccion.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es requerido', 'error')
            return redirect(url_for('secciones.editar', id=id))
            
        seccion.nombre = nombre
        db.session.commit()
        flash('Sección actualizada', 'success')
        return redirect(url_for('secciones.index'))
        
    return render_template('secciones/editar.html', seccion=seccion)

@secciones_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    seccion = Seccion.query.get_or_404(id)
    
    # Restricciones de integridad
    if seccion.estudiantes:
        flash('No se puede eliminar la sección porque tiene alumnos matriculados. Desvincula a los alumnos primero.', 'error')
        return redirect(url_for('secciones.index'))
        
    if seccion.asignaturas:
        flash('No se puede eliminar la sección porque está vinculada a asignaturas activas.', 'error')
        return redirect(url_for('secciones.index'))
        
    db.session.delete(seccion)
    db.session.commit()
    flash('Sección eliminada correctamente', 'success')
    return redirect(url_for('secciones.index'))

@secciones_bp.route('/<int:seccion_id>/crear_matricular', methods=['POST'])
def crear_y_matricular(seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    
    nie = request.form.get('nie')
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    genero = request.form.get('genero')
    
    if not nie or not nombres or not apellidos or not genero:
        flash('Todos los campos son requeridos para agregar un alumno manually', 'error')
        return redirect(url_for('secciones.detalle', id=seccion.id))
        
    est = Estudiante.query.filter_by(nie=nie).first()
    if not est:
        est = Estudiante(nie=nie, nombres=nombres, apellidos=apellidos, genero=genero)
        db.session.add(est)
        
    if est not in seccion.estudiantes:
        seccion.estudiantes.append(est)
        db.session.commit()
        flash('Estudiante añadido y matriculado exitosamente en el grupo.', 'success')
    else:
        db.session.commit() # por si se creo nuevo localmente (aunque el if asegura agregarlo al seccion en otro caso, pero bueno)
        flash('El estudiante ya estaba registrado y matriculado en el grupo.', 'success')
        
    return redirect(url_for('secciones.detalle', id=seccion.id))

@secciones_bp.route('/<int:seccion_id>/importar', methods=['POST'])
def importar_estudiantes(seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    file = request.files.get('archivo_csv')
    
    if not file or file.filename == '':
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('secciones.detalle', id=seccion.id))
        
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    
    registrados_nuevos = 0
    matriculados = 0
    header_skipped = False
    
    for row in csv_input:
        if not header_skipped:
            if 'nie' in str(row).lower() or 'nombre' in str(row).lower():
                header_skipped = True
                continue
                
        if len(row) >= 4:
            nie = str(row[0]).strip()
            nombres = str(row[1]).strip()
            apellidos = str(row[2]).strip()
            genero = str(row[3]).strip()
            
            if not nie:
                continue
                
            est = Estudiante.query.filter_by(nie=nie).first()
            if not est:
                est = Estudiante(nie=nie, nombres=nombres, apellidos=apellidos, genero=genero)
                db.session.add(est)
                registrados_nuevos += 1
                
            if est not in seccion.estudiantes:
                seccion.estudiantes.append(est)
                matriculados += 1
                
    db.session.commit()
    flash(f'Carga masiva completada: {matriculados} matriculados ({registrados_nuevos} estudiantes creados desde cero).', 'success')
    return redirect(url_for('secciones.detalle', id=seccion.id))

@secciones_bp.route('/<int:seccion_id>/remover_estudiante/<int:est_id>', methods=['POST'])
def remover_estudiante(seccion_id, est_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    est = Estudiante.query.get_or_404(est_id)
    if est in seccion.estudiantes:
        seccion.estudiantes.remove(est)
        db.session.commit()
        flash('Estudiante removido de la sección', 'success')
    return redirect(url_for('secciones.detalle', id=seccion.id))
