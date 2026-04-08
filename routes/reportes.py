from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Asignatura, Seccion, Estudiante, Periodo, Nota, Actividad, NotaRecuperacion
from extensions import db

reportes_bp = Blueprint('reportes', __name__)

def calcular_resumen_asignatura(asignatura, seccion):
    """
    Calcula el resumen de notas para todos los estudiantes de una sección en una asignatura.
    """
    periodos = asignatura.periodos
    estudiantes = seccion.estudiantes
    
    # Pre-cargar todas las notas y recuperaciones para evitar N+1
    notas_db = Nota.query.join(Actividad).join(Periodo).filter(Periodo.asignatura_id == asignatura.id).all()
    recuperaciones_db = NotaRecuperacion.query.join(Periodo).filter(Periodo.asignatura_id == asignatura.id).all()
    
    # Organizar en diccionarios para acceso rápido
    # {est_id: {act_id: valor}}
    mapa_notas = {}
    for n in notas_db:
        if n.estudiante_id not in mapa_notas: mapa_notas[n.estudiante_id] = {}
        mapa_notas[n.estudiante_id][n.actividad_id] = n.valor
        
    # {est_id: {per_id: valor}}
    mapa_recup = {}
    for r in recuperaciones_db:
        if r.estudiante_id not in mapa_recup: mapa_recup[r.estudiante_id] = {}
        mapa_recup[r.estudiante_id][r.periodo_id] = r.valor

    resumen = []
    
    for est in estudiantes:
        fila = {
            'estudiante': est,
            'periodos': [],
            'nota_final': 0.0
        }
        
        total_acumulado_asignatura = 0.0
        
        for per in periodos:
            subtotal_periodo = 0.0
            for act in per.actividades:
                nota_val = mapa_notas.get(est.id, {}).get(act.id, 0.0)
                subtotal_periodo += (nota_val * (act.ponderacion / 100))
            
            # Aplicar Lógica de Recuperación (Topada a 6.0)
            recup_val = mapa_recup.get(est.id, {}).get(per.id, None)
            nota_periodo_final = subtotal_periodo
            
            if subtotal_periodo < 6.0 and recup_val is not None:
                # El valor de recuperación se topa a 6.0
                recup_topada = min(recup_val, 6.0)
                # Si el estudiante recuperó, la nota del periodo es el máximo entre lo que tenía y la recuperación topada
                nota_periodo_final = max(subtotal_periodo, recup_topada)
            
            fila['periodos'].append({
                'periodo': per,
                'raw': subtotal_periodo,
                'recuperacion': recup_val,
                'final': nota_periodo_final
            })
            
            total_acumulado_asignatura += nota_periodo_final
            
        # Dependiendo de cómo se estructuren los periodos, la nota final podría ser el promedio de periodos
        # o la suma si los pesos de actividades son globales. 
        # Siguiendo la lógica del grid: es la suma acumulada de lo obtenido en cada periodo.
        # Si hay 3 periodos y cada uno suma hasta 10, la suma daría 30. 
        # No obstante, usualmente se promedia si los periodos son trimestres.
        # Vamos a promediar los resultados de los periodos para la nota final base 10.
        if len(periodos) > 0:
            fila['nota_final'] = total_acumulado_asignatura / len(periodos)
        else:
            fila['nota_final'] = 0.0
            
        fila['aprobado'] = fila['nota_final'] >= 6.0
        resumen.append(fila)
        
    return resumen

@reportes_bp.route('/')
def index():
    asignaturas = Asignatura.query.all()
    secciones = Seccion.query.all()
    estudiantes = Estudiante.query.order_by(Estudiante.apellidos).all()
    return render_template('reportes/index.html', 
                           asignaturas=asignaturas, 
                           secciones=secciones, 
                           estudiantes=estudiantes)

@reportes_bp.route('/asignatura/<int:asignatura_id>/<int:seccion_id>')
def reporte_asignatura(asignatura_id, seccion_id):
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    seccion = Seccion.query.get_or_404(seccion_id)
    
    resumen = calcular_resumen_asignatura(asignatura, seccion)
    
    return render_template('reportes/asignatura.html', 
                           asignatura=asignatura, 
                           seccion=seccion, 
                           resumen=resumen)

@reportes_bp.route('/seccion/<int:seccion_id>')
def reporte_seccion(seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    asignaturas = seccion.asignaturas
    
    # Matriz: Estudiante -> {Asignatura: NotaFinal}
    matriz = []
    for est in seccion.estudiantes:
        fila = {'estudiante': est, 'notas': []}
        promedio_general = 0.0
        
        for asig in asignaturas:
            # Reutilizar lógica de cálculo
            # Esto puede ser lento, pero para pocos datos funciona. 
            # Optimizamos filtrando solo para este estudiante.
            res_indiv = calcular_resumen_asignatura(asig, seccion)
            nota_est = next((r['nota_final'] for r in res_indiv if r['estudiante'].id == est.id), 0.0)
            fila['notas'].append({'asignatura': asig, 'nota': nota_est})
            promedio_general += nota_est
            
        if len(asignaturas) > 0:
            fila['promedio_general'] = promedio_general / len(asignaturas)
        else:
            fila['promedio_general'] = 0.0
            
        matriz.append(fila)
        
    return render_template('reportes/seccion.html', seccion=seccion, matriz=matriz, asignaturas=asignaturas)

@reportes_bp.route('/estudiante/<int:estudiante_id>')
def reporte_estudiante(estudiante_id):
    est = Estudiante.query.get_or_404(estudiante_id)
    # Obtener todas las secciones donde está matriculado
    secciones = est.secciones
    
    reporte_completo = []
    
    for sec in secciones:
        for asig in sec.asignaturas:
            res = calcular_resumen_asignatura(asig, sec)
            datos_est = next((r for r in res if r['estudiante'].id == est.id), None)
            if datos_est:
                reporte_completo.append({
                    'asignatura': asig,
                    'seccion': sec,
                    'detalle': datos_est
                })
                
    return render_template('reportes/estudiante.html', estudiante=est, reporte=reporte_completo)
