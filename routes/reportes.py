from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models import Asignatura, Seccion, Estudiante, Periodo, Nota, Actividad, NotaRecuperacion
from extensions import db
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

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
                
    max_periodos = 0
    if reporte_completo:
        max_periodos = max(len(item['detalle']['periodos']) for item in reporte_completo)
                
    return render_template('reportes/estudiante.html', estudiante=est, reporte=reporte_completo, max_periodos=max_periodos)

@reportes_bp.route('/exportar_excel/<int:asignatura_id>/<int:seccion_id>')
def exportar_excel(asignatura_id, seccion_id):
    asignatura = Asignatura.query.get_or_404(asignatura_id)
    seccion = Seccion.query.get_or_404(seccion_id)
    resumen = calcular_resumen_asignatura(asignatura, seccion)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Cuadro de Calificaciones"
    
    # Estilos
    font_bold = Font(bold=True)
    font_header = Font(bold=True, color="FFFFFF", size=12)
    fill_header = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
    fill_subheader = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center")
    border_thin = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    # Encabezado Institucional
    ws.merge_cells('A1:L1')
    ws['A1'] = "INSTITUTO NACIONAL DE SANTA ELENA"
    ws['A1'].font = Font(bold=True, size=16)
    ws['A1'].alignment = align_center
    
    ws.merge_cells('A2:L2')
    ws['A2'] = f"CUADRO DE CALIFICACIONES: {asignatura.nombre} - SECCIÓN: {seccion.nombre}"
    ws['A2'].font = Font(bold=True, size=12)
    ws['A2'].alignment = align_center
    
    # Fila de Encabezados de Tabla
    headers = ["NIE", "Apellidos y Nombres"]
    # Agregar periodos a los headers
    for p in asignatura.periodos:
        headers.append(f"{p.nombre} (P.)")
    headers.append("NOTA FINAL")
    headers.append("ESTADO")
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_num)
        cell.value = header
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_thin

    # Llenado de Datos
    for row_num, fila in enumerate(resumen, 5):
        ws.cell(row=row_num, column=1, value=fila['estudiante'].nie).border = border_thin
        ws.cell(row=row_num, column=2, value=f"{fila['estudiante'].apellidos}, {fila['estudiante'].nombres}").border = border_thin
        
        col_idx = 3
        for p_data in fila['periodos']:
            cell_p = ws.cell(row=row_num, column=col_idx, value=round(p_data['final'], 2))
            cell_p.border = border_thin
            cell_p.alignment = align_center
            col_idx += 1
            
        # Nota Final
        cell_final = ws.cell(row=row_num, column=col_idx, value=round(fila['nota_final'], 2))
        cell_final.border = border_thin
        cell_final.font = font_bold
        cell_final.alignment = align_center
        col_idx += 1
        
        # Estado
        estado = "APROBADO" if fila['nota_final'] >= 6.0 else "REPROBADO"
        cell_estado = ws.cell(row=row_num, column=col_idx, value=estado)
        cell_estado.border = border_thin
        cell_estado.alignment = align_center
        if estado == "REPROBADO":
            cell_estado.font = Font(color="FF0000", bold=True)
        else:
            cell_estado.font = Font(color="008000", bold=True)

    # Ajustar anchos de columnas
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 40
    for col_char in ['C', 'D', 'E', 'F', 'G']:
        ws.column_dimensions[col_char].width = 15

    # Guardar en memoria
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"Notas_{asignatura.nombre}_{seccion.nombre}.xlsx".replace(" ", "_")
    
    return send_file(output, 
                     download_name=filename, 
                     as_attachment=True, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@reportes_bp.route('/exportar_consolidado_excel/<int:seccion_id>')
def exportar_consolidado_excel(seccion_id):
    seccion = Seccion.query.get_or_404(seccion_id)
    estudiantes = seccion.estudiantes
    asignaturas = seccion.asignaturas
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Consolidado de Sección"
    
    # Estilos
    font_bold = Font(bold=True)
    font_header = Font(bold=True, color="FFFFFF", size=10)
    fill_header = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center")
    border_thin = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    # Encabezado Institucional
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(asignaturas) + 2)
    ws['A1'] = "INSTITUTO NACIONAL DE SANTA ELENA"
    ws['A1'].font = Font(bold=True, size=16)
    ws['A1'].alignment = align_center
    
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(asignaturas) + 2)
    ws['A2'] = f"REPORTE CONSOLIDADO: {seccion.nombre}"
    ws['A2'].font = Font(bold=True, size=12)
    ws['A2'].alignment = align_center

    # Encabezados de Tabla
    headers = ["N°", "Estudiante (Apellidos, Nombres)"]
    for asig in asignaturas:
        headers.append(asig.nombre)
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_num)
        cell.value = header
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_thin

    # Matriz de Datos
    for row_idx, est in enumerate(estudiantes, 5):
        ws.cell(row=row_idx, column=1, value=row_idx-4).border = border_thin
        ws.cell(row=row_idx, column=2, value=f"{est.apellidos}, {est.nombres}").border = border_thin
        
        for col_idx, asig in enumerate(asignaturas, 3):
            # Calcular nota final de esta materia para este estudiante
            data_res = calcular_resumen_asignatura(asig, seccion)
            # Buscar al estudiante en el resumen
            est_data = next((f for f in data_res if f['estudiante'].id == est.id), None)
            
            nota = est_data['nota_final'] if est_data else 0
            cell_n = ws.cell(row=row_idx, column=col_idx, value=round(nota, 2))
            cell_n.border = border_thin
            cell_n.alignment = align_center
            
            if nota < 6.0:
                cell_n.font = Font(color="FF0000")
        
    # Ajustar dimensiones
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 40
    for col_idx in range(3, len(asignaturas) + 3):
        ws.column_dimensions[ws.cell(row=4, column=col_idx).column_letter].width = 15

    # Guardar y enviar
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"Consolidado_{seccion.nombre}.xlsx".replace(" ", "_")
    return send_file(output, 
                     download_name=filename, 
                     as_attachment=True, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@reportes_bp.route('/planificacion/<int:periodo_id>')
def reporte_planificacion(periodo_id):
    periodo = Periodo.query.get_or_404(periodo_id)
    asignatura = periodo.asignatura
    from datetime import datetime
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    return render_template('reportes/planificacion.html', periodo=periodo, asignatura=asignatura, now=now)

@reportes_bp.route('/rubrica/<int:actividad_id>')
def reporte_rubrica(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    periodo = actividad.periodo
    asignatura = periodo.asignatura
    from datetime import datetime
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    return render_template('reportes/rubrica_print.html', actividad=actividad, periodo=periodo, asignatura=asignatura, now=now)
