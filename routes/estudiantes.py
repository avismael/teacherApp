import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Estudiante
from extensions import db

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        apellidos = request.form.get('apellidos')
        nombres = request.form.get('nombres')
        nie = request.form.get('nie')
        genero = request.form.get('genero')
        
        if not apellidos or not nombres or not nie or not genero:
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('estudiantes.index'))
            
        existente = Estudiante.query.filter_by(nie=nie).first()
        if existente:
            flash('Ya existe un estudiante con ese NIE', 'error')
            return redirect(url_for('estudiantes.index'))
            
        nuevo = Estudiante(apellidos=apellidos, nombres=nombres, nie=nie, genero=genero)
        db.session.add(nuevo)
        db.session.commit()
        flash('Estudiante registrado exitosamente', 'success')
        return redirect(url_for('estudiantes.index'))
        
    estudiantes = Estudiante.query.order_by(Estudiante.apellidos).all()
    
    # Calcular estadísticas
    total_estudiantes = len(estudiantes)
    total_masculinos = sum(1 for e in estudiantes if e.genero == 'Masculino')
    total_femeninos = sum(1 for e in estudiantes if e.genero == 'Femenino')
    total_otros = total_estudiantes - total_masculinos - total_femeninos
    
    stats = {
        'total': total_estudiantes,
        'masculinos': total_masculinos,
        'femeninos': total_femeninos,
        'otros': total_otros
    }
    
    return render_template('estudiantes/index.html', estudiantes=estudiantes, stats=stats)

@estudiantes_bp.route('/importar', methods=['POST'])
def importar_csv():
    file = request.files.get('archivo_csv')
    if not file or file.filename == '':
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('estudiantes.index'))
        
    if not file.filename.endswith('.csv'):
        flash('El archivo debe ser un CSV', 'error')
        return redirect(url_for('estudiantes.index'))
    
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    
    # Asumimos que la primera fila podría ser encabezados
    # Formato esperado: NIE, Nombres, Apellidos, Genero
    registrados = 0
    errores = 0
    header_skipped = False
    
    for indice, row in enumerate(csv_input):
        if not header_skipped: # Skip header (opcional, validando si parece encabezado)
            if 'nie' in str(row).lower() or 'nombre' in str(row).lower():
                header_skipped = True
                continue
                
        if len(row) >= 4:
            nie = str(row[0]).strip()
            nombres = str(row[1]).strip()
            apellidos = str(row[2]).strip()
            genero = str(row[3]).strip()
            
            # Verificar duplicado
            ext = Estudiante.query.filter_by(nie=nie).first()
            if not ext and nie:
                nuevo = Estudiante(nie=nie, nombres=nombres, apellidos=apellidos, genero=genero)
                db.session.add(nuevo)
                registrados += 1
            else:
                errores += 1
        else:
            errores += 1
            
    db.session.commit()
    flash(f'Importación masiva completada: {registrados} registrados, {errores} omitidos/duplicados.', 'success')
    return redirect(url_for('estudiantes.index'))
