from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from models import Periodo, Asignatura, Actividad, RubricaCriterio, RubricaNivel
from extensions import db

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/asignatura/<int:asignatura_id>/periodos', methods=['POST'])
def crear_periodo(asignatura_id):
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    nombre = request.form.get('nombre')
    if nombre:
        periodo = Periodo(nombre=nombre, asignatura_id=asignatura.id)
        db.session.add(periodo)
        db.session.commit()
        flash('Periodo creado exitosamente', 'success')
    return redirect(url_for('asignaturas.detalle', id=asignatura.id))

@evaluaciones_bp.route('/periodo/<int:periodo_id>/actividades', methods=['POST'])
def crear_actividad(periodo_id):
    periodo = Periodo.query.get_or_404(periodo_id)
    
    nombre = request.form.get('nombre')
    ponderacion = request.form.get('ponderacion', type=float)
    
    if not nombre or ponderacion is None:
        flash('Faltan datos para crear la actividad', 'error')
        return redirect(url_for('asignaturas.detalle', id=periodo.asignatura_id))
        
    actividades_existentes = Actividad.query.filter_by(periodo_id=periodo.id).all()
    suma_actual = sum(a.ponderacion for a in actividades_existentes)
    
    if suma_actual + ponderacion > 100.0:
        flash(f'Error: La suma ({suma_actual + ponderacion}%) excedería el 100% para este periodo (Máximo permitido es 100%).', 'error')
    else:
        act = Actividad(nombre=nombre, ponderacion=ponderacion, periodo_id=periodo.id)
        db.session.add(act)
        db.session.commit()
        flash('Actividad evaluativa creada para este periodo.', 'success')
        
    return redirect(url_for('asignaturas.detalle', id=periodo.asignatura_id))

@evaluaciones_bp.route('/actividad/<int:actividad_id>/rubrica', methods=['GET'])
def rubrica_builder(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    return render_template('evaluaciones/rubrica_builder.html', actividad=actividad)

@evaluaciones_bp.route('/actividad/<int:actividad_id>/rubrica/guardar', methods=['POST'])
def guardar_rubrica(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    data = request.json
    
    # Usar eliminación directa de la relación para asegurar que los cascades de SQLAlchemy funcionen
    for crit in actividad.criterios[:]:
        db.session.delete(crit)
    db.session.flush()
    
    for crit_data in data.get('criterios', []):
        crit = RubricaCriterio(nombre=crit_data['nombre'], actividad_id=actividad.id)
        db.session.add(crit)
        db.session.flush()
        
        for niv_data in crit_data.get('niveles', []):
            niv = RubricaNivel(
                nombre=niv_data['nombre'],
                descripcion=niv_data.get('descripcion', ''),
                puntaje=float(niv_data['puntaje']),
                criterio_id=crit.id
            )
            db.session.add(niv)
            
    db.session.commit()
    return jsonify({"success": True})

@evaluaciones_bp.route('/actividad/<int:actividad_id>/rubrica/csv', methods=['POST'])
def importar_rubrica_csv(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    if 'csv_file' not in request.files:
        flash('No se subió archivo CSV', 'error')
        return redirect(url_for('evaluaciones.rubrica_builder', actividad_id=actividad.id))
        
    file = request.files['csv_file']
    if file.filename == '':
        flash('El archivo está vacío', 'error')
        return redirect(url_for('evaluaciones.rubrica_builder', actividad_id=actividad.id))
        
    import csv
    import io
    
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.reader(stream)
    
    # Estructura: Criterio, Nivel, Puntos, Descripcion
    for crit in actividad.criterios[:]:
        db.session.delete(crit)
    db.session.flush()
    
    criterios_dict = {}
    
    header_skipped = False
    for row in csv_reader:
        if not header_skipped:
            header_skipped = True
            if 'criterio' in row[0].lower(): # Simple header check
                continue
                
        if len(row) >= 3:
            crit_name = row[0].strip()
            niv_name = row[1].strip()
            try:
                puntaje = float(row[2].strip().replace(',', '.'))
            except ValueError:
                continue
            desc = row[3].strip() if len(row) > 3 else ""
            
            if crit_name not in criterios_dict:
                crit = RubricaCriterio(nombre=crit_name, actividad_id=actividad.id)
                db.session.add(crit)
                db.session.flush()
                criterios_dict[crit_name] = crit
            else:
                crit = criterios_dict[crit_name]
                
            niv = RubricaNivel(nombre=niv_name, descripcion=desc, puntaje=puntaje, criterio_id=crit.id)
            db.session.add(niv)
            
    db.session.commit()
    flash('Rúbrica importada exitosamente desde CSV', 'success')
    return redirect(url_for('evaluaciones.rubrica_builder', actividad_id=actividad.id))
