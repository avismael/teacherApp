import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from models import Seccion, Estudiante, Asistencia, AsistenciaDetalle
from extensions import db
from xhtml2pdf import pisa
import io

asistencia_bp = Blueprint('asistencia', __name__)

@asistencia_bp.route('/')
def index():
    secciones = Seccion.query.all()
    return render_template('asistencia/index.html', secciones=secciones)

@asistencia_bp.route('/tomar/<int:seccion_id>', methods=['GET'])
def tomar(seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    estudiantes = sorted(seccion.estudiantes, key=lambda x: x.apellidos)
    now = datetime.now()
    return render_template('asistencia/tomar.html', 
                           seccion=seccion, 
                           estudiantes=estudiantes, 
                           fecha_actual=now.strftime('%Y-%m-%d'),
                           hora_actual=now.strftime('%H:%M'))

@asistencia_bp.route('/guardar', methods=['POST'])
def guardar():
    seccion_id = request.form.get('seccion_id')
    fecha_str = request.form.get('fecha')
    hora_str = request.form.get('hora')
    turno = request.form.get('turno')
    
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    hora = datetime.strptime(hora_str, '%H:%M').time()
    
    # Crear cabecera
    nueva_asistencia = Asistencia(
        seccion_id=seccion_id,
        fecha=fecha,
        hora=hora,
        turno=turno
    )
    db.session.add(nueva_asistencia)
    db.session.flush() # Para obtener el ID
    
    # Procesar estudiantes
    seccion = Seccion.query.get(seccion_id)
    for est in seccion.estudiantes:
        estado = request.form.get(f'estado_{est.id}')
        if not estado: continue
        
        nota = request.form.get(f'nota_{est.id}', '')
        archivo = request.files.get(f'archivo_{est.id}')
        nombre_archivo = None
        
        if archivo and archivo.filename != '':
            ext = os.path.splitext(archivo.filename)[1]
            nombre_archivo = f"{uuid.uuid4()}{ext}"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER_ASISTENCIA'], nombre_archivo)
            archivo.save(upload_path)
            
        detalle = AsistenciaDetalle(
            asistencia_id=nueva_asistencia.id,
            estudiante_id=est.id,
            estado=estado,
            nota=nota,
            archivo_justificacion=nombre_archivo
        )
        db.session.add(detalle)
        
    db.session.commit()
    flash('Asistencia guardada correctamente', 'success')
    return redirect(url_for('asistencia.historial'))

@asistencia_bp.route('/historial')
def historial():
    q = request.args.get('q', '')
    if q:
        # Búsqueda por nombre de sección o fecha (formato YYYY-MM-DD)
        asistencias = Asistencia.query.join(Seccion).filter(
            (Seccion.nombre.ilike(f'%{q}%')) | 
            (db.cast(Asistencia.fecha, db.String).ilike(f'%{q}%'))
        ).order_by(Asistencia.fecha.desc(), Asistencia.hora.desc()).all()
    else:
        asistencias = Asistencia.query.order_by(Asistencia.fecha.desc(), Asistencia.hora.desc()).all()
        
    return render_template('asistencia/historial.html', asistencias=asistencias, q=q)

@asistencia_bp.route('/detalle/<int:id>')
def detalle(id):
    asistencia = Asistencia.query.get_or_404(id)
    # Estadísticas
    stats = {
        'Presente': {'total': 0, 'M': 0, 'F': 0},
        'Ausente': {'total': 0, 'M': 0, 'F': 0},
        'Permiso': {'total': 0, 'M': 0, 'F': 0},
        'Escape': {'total': 0, 'M': 0, 'F': 0}
    }
    for d in asistencia.detalles:
        stats[d.estado]['total'] += 1
        gen = d.estudiante.genero.upper() if d.estudiante.genero else ''
        if gen in ['MASCULINO', 'M']:
            stats[d.estado]['M'] += 1
        elif gen in ['FEMENINO', 'F']:
            stats[d.estado]['F'] += 1
        
    return render_template('asistencia/detalle.html', asistencia=asistencia, stats=stats)

@asistencia_bp.route('/reporte_pdf/<int:id>')
def reporte_pdf(id):
    asistencia = Asistencia.query.get_or_404(id)
    stats = {
        'Presente': {'total': 0, 'M': 0, 'F': 0},
        'Ausente': {'total': 0, 'M': 0, 'F': 0},
        'Permiso': {'total': 0, 'M': 0, 'F': 0},
        'Escape': {'total': 0, 'M': 0, 'F': 0}
    }
    for d in asistencia.detalles:
        stats[d.estado]['total'] += 1
        gen = d.estudiante.genero.upper() if d.estudiante.genero else ''
        if gen in ['MASCULINO', 'M']:
            stats[d.estado]['M'] += 1
        elif gen in ['FEMENINO', 'F']:
            stats[d.estado]['F'] += 1
        
    html = render_template('asistencia/reporte_pdf.html', asistencia=asistencia, stats=stats)
    
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        result.seek(0)
        filename = f"Asistencia_{asistencia.seccion.nombre}_{asistencia.fecha}.pdf".replace(" ", "_")
        return send_file(result, download_name=filename, as_attachment=True, mimetype='application/pdf')
    
    flash('Error al generar el PDF', 'error')
    return redirect(url_for('asistencia.detalle', id=id))

@asistencia_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    asistencia = Asistencia.query.get_or_404(id)
    seccion = asistencia.seccion
    estudiantes = sorted(seccion.estudiantes, key=lambda x: x.apellidos)
    
    if request.method == 'POST':
        asistencia.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date()
        asistencia.hora = datetime.strptime(request.form.get('hora'), '%H:%M').time()
        asistencia.turno = request.form.get('turno')
        
        # Procesar actualizaciones de detalles
        detalles_dict = {d.estudiante_id: d for d in asistencia.detalles}
        
        for est in estudiantes:
            estado = request.form.get(f'estado_{est.id}')
            if not estado: continue
            
            nota = request.form.get(f'nota_{est.id}', '')
            archivo = request.files.get(f'archivo_{est.id}')
            
            detalle = detalles_dict.get(est.id)
            if not detalle:
                # Esto no debería pasar usualmente si la sección es la misma
                detalle = AsistenciaDetalle(asistencia_id=asistencia.id, estudiante_id=est.id)
                db.session.add(detalle)
            
            detalle.estado = estado
            detalle.nota = nota
            
            if archivo and archivo.filename != '':
                # Eliminar archivo viejo si existe
                if detalle.archivo_justificacion:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER_ASISTENCIA'], detalle.archivo_justificacion)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                ext = os.path.splitext(archivo.filename)[1]
                nombre_archivo = f"{uuid.uuid4()}{ext}"
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER_ASISTENCIA'], nombre_archivo)
                archivo.save(upload_path)
                detalle.archivo_justificacion = nombre_archivo
        
        db.session.commit()
        flash('Asistencia actualizada correctamente', 'success')
        return redirect(url_for('asistencia.detalle', id=asistencia.id))
        
    return render_template('asistencia/editar.html', 
                           asistencia=asistencia, 
                           seccion=seccion, 
                           estudiantes=estudiantes)

@asistencia_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    asistencia = Asistencia.query.get_or_404(id)
    
    # Eliminar archivos adjuntos
    for det in asistencia.detalles:
        if det.archivo_justificacion:
            path = os.path.join(current_app.config['UPLOAD_FOLDER_ASISTENCIA'], det.archivo_justificacion)
            if os.path.exists(path):
                os.remove(path)
                
    db.session.delete(asistencia)
    db.session.commit()
    flash('Registro de asistencia eliminado correctamente', 'success')
    return redirect(url_for('asistencia.historial'))
