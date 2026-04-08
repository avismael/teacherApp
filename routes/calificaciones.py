from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Seccion, Asignatura, Actividad, Nota, Periodo
from extensions import db

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/grid/<int:asignatura_id>/<int:seccion_id>', methods=['GET'])
def modificar_grid(asignatura_id, seccion_id):
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    seccion = Seccion.query.get_or_404(seccion_id)
    
    if seccion not in asignatura.secciones:
        flash('Esta sección no está matriculada en la asignatura seleccionada.', 'error')
        return redirect(url_for('asignaturas.detalle', id=asignatura.id))

    periodos = asignatura.periodos
    
    # Pre-cargar notas
    # Obtener todas las notas de esta asignatura (a través de periodos y actividades)
    notas_db = Nota.query.join(Actividad).join(Periodo).filter(Periodo.asignatura_id == asignatura.id).all()
    notas_dict = {}
    for n in notas_db:
        if n.estudiante_id not in notas_dict:
            notas_dict[n.estudiante_id] = {}
        notas_dict[n.estudiante_id][n.actividad_id] = n.valor

    # Obtener notas de recup
    from models import NotaRecuperacion
    recup_db = NotaRecuperacion.query.join(Periodo).filter(Periodo.asignatura_id == asignatura.id).all()
    recup_dict = {}
    for r in recup_db:
        if r.estudiante_id not in recup_dict:
            recup_dict[r.estudiante_id] = {}
        recup_dict[r.estudiante_id][r.periodo_id] = r.valor

    return render_template('calificaciones/grid.html', 
        seccion=seccion, 
        asignatura=asignatura, 
        periodos=periodos,
        notas_dict=notas_dict,
        recup_dict=recup_dict)

@calificaciones_bp.route('/grid/<int:asignatura_id>/<int:seccion_id>/guardar', methods=['POST'])
def guardar_notas(asignatura_id, seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    
    for key, value in request.form.items():
        if key.startswith('nota_') and value.strip() != '':
            try:
                parts = key.split('_')
                est_id = int(parts[1])
                act_id = int(parts[2])
                val_float = float(value.replace(',', '.'))
                
                # Validar que el estudiante pertenece a la sección y la actividad a la asignatura (opcional pero más seguro)
                nota = Nota.query.filter_by(estudiante_id=est_id, actividad_id=act_id).first()
                if nota:
                    nota.valor = val_float
                else:
                    nota = Nota(estudiante_id=est_id, actividad_id=act_id, valor=val_float)
                    db.session.add(nota)
            except Exception as e:
                pass
                
        # Capturar notas de recuperación
        elif key.startswith('recup_') and value.strip() != '':
            try:
                from models import NotaRecuperacion
                parts = key.split('_')
                est_id = int(parts[1])
                per_id = int(parts[2])
                val_float = float(value.replace(',', '.'))
                
                # Topar a 6.0 lógicamente en la BD por si acaso, o guardar tal cual y pintar el tope.
                # Como tu regla dice "topa a 6.0 automáticamente", lo forzamos.
                if val_float > 6.0:
                    val_float = 6.0
                    
                rec_nota = NotaRecuperacion.query.filter_by(estudiante_id=est_id, periodo_id=per_id).first()
                if rec_nota:
                    rec_nota.valor = val_float
                else:
                    rec_nota = NotaRecuperacion(estudiante_id=est_id, periodo_id=per_id, valor=val_float)
                    db.session.add(rec_nota)
            except Exception as e:
                pass

    db.session.commit()
    flash('Calificaciones actualizadas correctamente.', 'success')
    return redirect(url_for('calificaciones.modificar_grid', asignatura_id=asignatura.id, seccion_id=seccion.id))

@calificaciones_bp.route('/api/rubrica/<int:actividad_id>/<int:estudiante_id>', methods=['GET'])
def get_rubrica_estudiante(actividad_id, estudiante_id):
    from models import RubricaCriterio, RubricaEvaluacion
    
    actividad = Actividad.query.get_or_404(actividad_id)
    evaluaciones = RubricaEvaluacion.query.filter_by(estudiante_id=estudiante_id, actividad_id=actividad_id).all()
    
    # Mapa_evaluado: criterio_id -> nivel_id elegido previamente
    eval_dict = { e.criterio_id: e.nivel_id for e in evaluaciones }
    
    criterios_json = []
    for c in actividad.criterios:
        criterios_json.append({
            "id": c.id,
            "nombre": c.nombre,
            "seleccionado": eval_dict.get(c.id, None),
            "niveles": [{"id": n.id, "nombre": n.nombre, "puntaje": n.puntaje, "descripcion": n.descripcion} for n in c.niveles]
        })
        
    return jsonify({
        "success": True,
        "actividadNombre": actividad.nombre,
        "criterios": criterios_json
    })

@calificaciones_bp.route('/api/rubrica/<int:actividad_id>/<int:estudiante_id>/guardar', methods=['POST'])
def guardar_rubrica_estudiante(actividad_id, estudiante_id):
    from models import RubricaEvaluacion, RubricaNivel
    
    actividad = Actividad.query.get_or_404(actividad_id)
    data = request.json # { selecciones: { criterio_id: nivel_id, ... } }
    
    # 1. Borrar eval anterior
    RubricaEvaluacion.query.filter_by(estudiante_id=estudiante_id, actividad_id=actividad_id).delete()
    
    # 2. Guardar selecciones y sumar puntos base
    puntaje_total = 0.0
    selecciones = data.get('selecciones', {})
    
    for str_crit_id, nivel_id in selecciones.items():
        if not nivel_id: continue
        try:
            crit_id = int(str_crit_id)
            niv_id = int(nivel_id)
            nivel_obj = RubricaNivel.query.get(niv_id)
            
            if nivel_obj:
                puntaje_total += nivel_obj.puntaje
                nueva_eval = RubricaEvaluacion(
                    estudiante_id=estudiante_id, 
                    actividad_id=actividad.id,
                    criterio_id=crit_id,
                    nivel_id=niv_id
                )
                db.session.add(nueva_eval)
        except:
            pass

    # El profe diseña los niveles para que max lleguen a 10. Pasamos la suma cruda al sistema final.
    nota_final = puntaje_total
    
    # Guardar en generico Nota
    nota_obj = Nota.query.filter_by(estudiante_id=estudiante_id, actividad_id=actividad.id).first()
    if nota_obj:
        nota_obj.valor = nota_final
    else:
        nota_obj = Nota(valor=nota_final, estudiante_id=estudiante_id, actividad_id=actividad.id)
        db.session.add(nota_obj)
        
    db.session.commit()
    
    return jsonify({
        "success": True,
        "nota_final": nota_final
    })
