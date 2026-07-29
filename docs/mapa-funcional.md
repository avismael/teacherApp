# Mapa Funcional - TeacherApp

## 1. Vista General

TeacherApp se organiza en ocho modulos funcionales principales conectados sobre un mismo modelo academico.

```text
Dashboard
  -> Asignaturas
    -> Periodos
      -> Actividades
        -> Rubricas
        -> Calificaciones
        -> Reportes
  -> Secciones
    -> Matricula de estudiantes
    -> Asistencia
    -> Reportes
  -> Estudiantes
    -> Historial academico
    -> Historial de asistencia
  -> Reportes
```

## 2. Mapa Por Modulo

### 2.1 Dashboard

Objetivo:
Concentrar la vista inicial del sistema.

Entradas:

1. Conteo de asignaturas.
2. Conteo de estudiantes.
3. Conteo de secciones.
4. Listado de asignaturas.

Salidas:

1. Indicadores generales.
2. Navegacion hacia modulos academicos.

Dependencias:

1. `Asignatura`
2. `Estudiante`
3. `Seccion`

### 2.2 Asignaturas

Objetivo:
Administrar las materias y su relacion con secciones y periodos.

Funciones:

1. Crear asignatura.
2. Editar asignatura.
3. Eliminar asignatura.
4. Ver detalle de asignatura.
5. Vincular seccion.
6. Desvincular seccion.

Objetos asociados:

1. `Asignatura`
2. `Seccion`
3. `Periodo`
4. `Actividad`

Reglas:

1. No eliminar si hay notas asociadas.
2. No desvincular una seccion si ya existen notas de sus estudiantes en la materia.

### 2.3 Secciones

Objetivo:
Gestionar grupos de estudiantes.

Funciones:

1. Crear seccion.
2. Editar seccion.
3. Eliminar seccion.
4. Ver detalle de seccion.
5. Crear y matricular estudiante.
6. Importar estudiantes por CSV.
7. Editar estudiante desde la seccion.
8. Eliminar estudiante.

Objetos asociados:

1. `Seccion`
2. `Estudiante`
3. `Asignatura`

Reglas:

1. No eliminar seccion con estudiantes matriculados.
2. No eliminar seccion vinculada a asignaturas.
3. Un estudiante no debe quedar matriculado en otra seccion distinta al intentar reasignar por esta via.

### 2.4 Estudiantes

Objetivo:
Gestionar el catalogo general de alumnos.

Funciones:

1. Crear estudiante manualmente.
2. Importar estudiantes por CSV.
3. Buscar por NIE, nombre, apellido o seccion.
4. Consultar estadisticas globales.

Objetos asociados:

1. `Estudiante`
2. `Seccion`

Reglas:

1. `NIE` unico.

### 2.5 Evaluaciones

Objetivo:
Definir la estructura de evaluacion por asignatura.

Funciones:

1. Crear periodo.
2. Editar periodo.
3. Eliminar periodo.
4. Crear actividad.
5. Editar actividad.
6. Eliminar actividad.

Objetos asociados:

1. `Periodo`
2. `Actividad`
3. `Asignatura`

Reglas:

1. La ponderacion acumulada por periodo no puede exceder 100.
2. Eliminar periodo elimina actividades y notas relacionadas.

### 2.6 Rubricas

Objetivo:
Permitir evaluaciones estructuradas por criterios y niveles.

Funciones:

1. Abrir constructor de rubrica.
2. Guardar rubrica completa.
3. Reemplazar rubrica existente.
4. Importar rubrica desde CSV.
5. Consultar rubrica por estudiante y actividad.
6. Guardar evaluacion de rubrica por estudiante.

Objetos asociados:

1. `Actividad`
2. `RubricaCriterio`
3. `RubricaNivel`
4. `RubricaEvaluacion`
5. `Nota`

Reglas:

1. La evaluacion por rubrica recalcula la nota de la actividad.
2. Guardar la rubrica reemplaza criterios y niveles anteriores.

### 2.7 Calificaciones

Objetivo:
Registrar y modificar notas de estudiantes por actividad y por recuperacion.

Funciones:

1. Abrir grid de notas.
2. Precargar notas existentes.
3. Guardar notas de actividad.
4. Guardar notas de recuperacion.
5. Evaluar por rubrica.

Objetos asociados:

1. `Nota`
2. `NotaRecuperacion`
3. `Actividad`
4. `Periodo`
5. `Estudiante`

Reglas:

1. La recuperacion se topa a 6.0.
2. La seccion debe estar vinculada a la asignatura para abrir el grid.

### 2.8 Asistencia

Objetivo:
Gestionar el control diario de presencia por seccion.

Funciones:

1. Seleccionar seccion para toma.
2. Registrar fecha, hora y turno.
3. Registrar estado por estudiante.
4. Adjuntar justificacion.
5. Consultar historial.
6. Ver detalle y estadisticas.
7. Editar registro.
8. Exportar PDF.
9. Eliminar registro.

Objetos asociados:

1. `Asistencia`
2. `AsistenciaDetalle`
3. `Seccion`
4. `Estudiante`

Estados manejados:

1. `Presente`
2. `Ausente`
3. `Permiso`
4. `Escape`

### 2.9 Reportes

Objetivo:
Consolidar resultados academicos y de asistencia.

Funciones:

1. Reporte por asignatura y seccion.
2. Reporte consolidado por seccion.
3. Reporte por estudiante.
4. Exportacion Excel por asignatura.
5. Exportacion Excel consolidada.
6. Reporte de planificacion.
7. Reporte imprimible de rubrica.
8. Reporte de asistencia por seccion.
9. Reporte de asistencia por estudiante.

Objetos asociados:

1. `Asignatura`
2. `Seccion`
3. `Estudiante`
4. `Periodo`
5. `Actividad`
6. `Nota`
7. `NotaRecuperacion`
8. `Asistencia`
9. `AsistenciaDetalle`

## 3. Mapa De Navegacion Principal

```text
Inicio (/)
  -> Asignaturas (/asignaturas/)
    -> Detalle de asignatura (/asignaturas/<id>)
      -> Crear periodo
      -> Crear actividad
      -> Editar periodo
      -> Editar actividad
      -> Builder de rubrica (/evaluaciones/actividad/<actividad_id>/rubrica)
      -> Grid de calificaciones (/calificaciones/grid/<asignatura_id>/<seccion_id>)

  -> Estudiantes (/estudiantes/)
    -> Importacion CSV

  -> Secciones (/secciones/)
    -> Detalle de seccion (/secciones/<id>)
      -> Crear y matricular estudiante
      -> Importar CSV
      -> Editar estudiante

  -> Asistencia (/asistencia/)
    -> Tomar asistencia (/asistencia/tomar/<seccion_id>)
    -> Historial (/asistencia/historial)
    -> Detalle (/asistencia/detalle/<id>)
    -> Editar (/asistencia/editar/<id>)
    -> PDF (/asistencia/reporte_pdf/<id>)

  -> Reportes (/reportes/)
    -> Asignatura (/reportes/asignatura/<asignatura_id>/<seccion_id>)
    -> Seccion (/reportes/seccion/<seccion_id>)
    -> Estudiante (/reportes/estudiante/<estudiante_id>)
    -> Excel (/reportes/exportar_excel/<asignatura_id>/<seccion_id>)
    -> Consolidado (/reportes/exportar_consolidado_excel/<seccion_id>)
    -> Planificacion (/reportes/planificacion/<periodo_id>)
    -> Rubrica imprimible (/reportes/rubrica/<actividad_id>)
    -> Asistencia seccion (/reportes/asistencia/seccion/<seccion_id>)
    -> Asistencia estudiante (/reportes/asistencia/estudiante/<estudiante_id>)
```

## 4. Mapa De Dependencias Funcionales

```text
Secciones -> Estudiantes
Asignaturas -> Secciones
Asignaturas -> Periodos -> Actividades
Actividades -> Notas
Actividades -> Rubricas -> Evaluacion por rubrica -> Nota
Periodos -> Recuperaciones
Secciones -> Asistencia -> Reportes de asistencia
Asignaturas + Secciones + Notas -> Reportes academicos
```

## 5. Flujo De Valor Docente

```text
Configurar estructura academica
  -> Matricular estudiantes
  -> Planificar evaluaciones
  -> Aplicar actividades
  -> Registrar notas
  -> Registrar recuperacion
  -> Tomar asistencia
  -> Consolidar resultados
  -> Exportar evidencias
```

## 6. Puntos Criticos Del Sistema

1. Integridad entre asignatura, seccion y estudiante antes de calificar.
2. Control de ponderaciones en actividades.
3. Reemplazo completo de rubricas al guardar.
4. Borrado con cascada de entidades academicas relacionadas.
5. Manejo de adjuntos de asistencia y limpieza al eliminar.
6. Consistencia del calculo final en reportes.
