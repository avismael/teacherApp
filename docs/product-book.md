# Product Book - TeacherApp

## 1. Resumen Ejecutivo

TeacherApp es una aplicacion web offline-first para la gestion academica docente. Permite administrar asignaturas, secciones, estudiantes, evaluaciones, calificaciones, recuperaciones, asistencia y reportes operativos desde una sola interfaz.

La solucion esta orientada a centros educativos que necesitan un registro estructurado de notas y asistencia sin depender de conectividad permanente. El sistema opera sobre Flask, SQLAlchemy y SQLite, con vistas HTML renderizadas en servidor.

## 2. Vision Del Producto

Centralizar el trabajo academico cotidiano del docente en una herramienta simple, rapida y consistente que reduzca tareas manuales, minimice errores de registro y facilite la generacion de evidencias academicas.

## 3. Problema Que Resuelve

La app resuelve tres problemas principales:

1. Fragmentacion del trabajo docente entre papel, hojas de calculo y registros informales.
2. Riesgo de inconsistencia entre estudiantes, secciones, asignaturas, notas y asistencia.
3. Dificultad para consolidar reportes individuales, grupales y exportables.

## 4. Objetivos Del Producto

1. Permitir registrar y consultar informacion academica por asignatura y seccion.
2. Estandarizar la evaluacion mediante actividades ponderadas y rubricas.
3. Gestionar recuperaciones por periodo con reglas de negocio definidas.
4. Registrar asistencia con soporte para observaciones y adjuntos.
5. Generar reportes operativos y exportaciones listas para uso institucional.

## 5. Usuarios Objetivo

### 5.1 Usuario Primario

Docente responsable de una o varias asignaturas y secciones.

Necesidades principales:

1. Crear estructura academica.
2. Matricular estudiantes.
3. Diseñar periodos y actividades.
4. Registrar notas y recuperaciones.
5. Tomar asistencia.
6. Emitir reportes.

### 5.2 Usuario Secundario

Coordinacion academica o apoyo administrativo con necesidad de consultar o exportar informacion consolidada.

## 6. Alcance Funcional Actual

### 6.1 Dashboard

1. Muestra conteos globales de asignaturas, estudiantes y secciones.
2. Lista asignaturas registradas como punto de acceso rapido.

### 6.2 Gestion De Asignaturas

1. Crear asignaturas.
2. Editar nombre y descripcion.
3. Eliminar asignaturas con restriccion si existen notas asociadas.
4. Vincular secciones a una asignatura.
5. Desvincular secciones con restriccion si ya existen notas de estudiantes de esa seccion en esa asignatura.

### 6.3 Gestion De Secciones

1. Crear secciones.
2. Editar secciones.
3. Eliminar secciones solo si no tienen estudiantes ni asignaturas vinculadas.
4. Ver detalle de seccion y su matricula.
5. Crear y matricular estudiante desde la seccion.
6. Importar estudiantes por CSV dentro de una seccion.
7. Editar datos de estudiante desde la vista de seccion.
8. Eliminar estudiante del sistema.

### 6.4 Gestion De Estudiantes

1. Crear estudiantes manualmente.
2. Buscar por NIE, nombres, apellidos o seccion.
3. Importar estudiantes por CSV.
4. Visualizar estadisticas globales por genero.

### 6.5 Evaluaciones

1. Crear periodos por asignatura.
2. Crear actividades por periodo.
3. Validar que la suma de ponderaciones por periodo no exceda 100.
4. Editar periodos y actividades.
5. Eliminar periodos con cascada sobre actividades y notas asociadas.
6. Eliminar actividades con cascada sobre notas asociadas.

### 6.6 Rubricas

1. Diseñar rubricas por actividad.
2. Guardar criterios y niveles desde interfaz JSON.
3. Reemplazar la rubrica completa al volver a guardar.
4. Importar rubricas desde CSV.

### 6.7 Calificaciones

1. Abrir grid de notas por asignatura y seccion.
2. Registrar o actualizar nota por actividad y estudiante.
3. Registrar notas de recuperacion por periodo.
4. Topar automaticamente la recuperacion a 6.0.
5. Evaluar estudiantes mediante rubrica y convertir niveles seleccionados en nota final de actividad.

### 6.8 Asistencia

1. Seleccionar seccion para toma de asistencia.
2. Registrar fecha, hora y turno.
3. Registrar estado por estudiante.
4. Agregar nota libre por estudiante.
5. Adjuntar archivo de justificacion por estudiante.
6. Consultar historial de asistencias.
7. Buscar historial por seccion o fecha.
8. Ver detalle con estadisticas por estado y genero.
9. Editar asistencia existente.
10. Generar PDF del registro de asistencia.
11. Eliminar asistencia y sus adjuntos.

### 6.9 Reportes

1. Reporte por asignatura y seccion.
2. Reporte consolidado por seccion.
3. Reporte individual por estudiante.
4. Reporte de planificacion por periodo.
5. Reporte imprimible de rubrica por actividad.
6. Reporte de asistencia por seccion.
7. Reporte de asistencia por estudiante.
8. Exportacion Excel de calificaciones por asignatura.
9. Exportacion Excel consolidada por seccion.

## 7. Reglas De Negocio Relevantes

1. El `NIE` del estudiante es unico.
2. Un estudiante no puede duplicar nota para la misma actividad.
3. Un estudiante no puede duplicar recuperacion para el mismo periodo.
4. Una evaluacion de rubrica es unica por estudiante y criterio.
5. La suma de ponderaciones de actividades dentro de un periodo no puede superar 100.
6. Una asignatura no puede eliminarse si existen notas asociadas a sus periodos y actividades.
7. Una seccion no puede eliminarse si tiene estudiantes matriculados.
8. Una seccion no puede eliminarse si esta vinculada a asignaturas activas.
9. Una seccion no puede desvincularse de una asignatura si ya hay notas de estudiantes de esa seccion en esa asignatura.
10. La nota de recuperacion se topa a 6.0.
11. La nota final por periodo usa el mayor valor entre subtotal y recuperacion topada, si el subtotal fue menor a 6.0.
12. La nota final de asignatura se calcula como promedio de periodos.
13. La eliminacion de periodos, actividades, rubricas, notas y asistencia usa cascadas para preservar integridad.

## 8. Flujo Operativo Esperado

1. Crear secciones.
2. Registrar estudiantes o importarlos.
3. Matricular estudiantes en secciones.
4. Crear asignaturas.
5. Vincular secciones a asignaturas.
6. Crear periodos por asignatura.
7. Crear actividades ponderadas por periodo.
8. Diseñar rubricas si aplica.
9. Registrar notas o evaluar por rubrica.
10. Registrar recuperaciones.
11. Tomar asistencia durante el periodo academico.
12. Consultar y exportar reportes.

## 9. Arquitectura Funcional

### 9.1 Frontend

1. Plantillas Jinja2 renderizadas por Flask.
2. Navegacion principal en `templates/base.html`.
3. JS ligero para sidebar y menu movil en `static/js/app.js`.
4. Estilos con Tailwind CSS compilado localmente.

### 9.2 Backend

1. Punto de entrada en `app.py`.
2. Blueprints modulares por dominio.
3. Logica de negocio distribuida dentro de rutas.
4. Persistencia con SQLAlchemy.

### 9.3 Persistencia

1. Base SQLite local.
2. Modelos ORM en `models.py`.
3. Creacion automatica de tablas con `db.create_all()`.
4. Almacenamiento de adjuntos de asistencia en `static/uploads/asistencia`.

## 10. Modulo De Datos

### 10.1 Entidades Principales

1. `Asignatura`
2. `Seccion`
3. `Estudiante`
4. `Periodo`
5. `Actividad`
6. `Nota`
7. `RubricaCriterio`
8. `RubricaNivel`
9. `RubricaEvaluacion`
10. `NotaRecuperacion`
11. `Asistencia`
12. `AsistenciaDetalle`

### 10.2 Relaciones Clave

1. Asignatura <-> Seccion es muchos a muchos.
2. Seccion <-> Estudiante es muchos a muchos.
3. Asignatura -> Periodo es uno a muchos.
4. Periodo -> Actividad es uno a muchos.
5. Actividad -> Nota es uno a muchos.
6. Actividad -> RubricaCriterio es uno a muchos.
7. RubricaCriterio -> RubricaNivel es uno a muchos.
8. Estudiante + Actividad -> Nota es una combinacion unica.
9. Estudiante + Periodo -> NotaRecuperacion es una combinacion unica.
10. Seccion -> Asistencia es uno a muchos.
11. Asistencia -> AsistenciaDetalle es uno a muchos.

## 11. Requisitos No Funcionales Observados

1. Operacion local y rapida sobre SQLite.
2. Disponibilidad offline de los activos principales.
3. Interfaz adaptada a escritorio y movil.
4. Exportaciones listas para descargar.
5. Integridad referencial apoyada en cascadas y validaciones de ruta.

## 12. Riesgos y Limitaciones Actuales

1. No existe autenticacion ni control de roles.
2. La logica de negocio esta concentrada mayormente en las rutas.
3. `db.create_all()` sugiere ausencia de migraciones formales.
4. SQLite es suficiente para uso local, pero limita escenarios multiusuario concurrentes.
5. No hay API externa formal; la app esta pensada como sistema web renderizado en servidor.
6. El borrado definitivo de estudiante desde secciones puede tener impacto amplio sobre historicos, aunque las cascadas mantienen consistencia tecnica.

## 13. Oportunidades De Evolucion

1. Incorporar usuarios, autenticacion y perfiles.
2. Separar servicios de negocio de las rutas.
3. Incorporar migraciones con Flask-Migrate o Alembic.
4. Añadir auditoria de cambios.
5. Agregar indicadores institucionales y paneles avanzados.
6. Permitir configuracion de escalas de nota y reglas de recuperacion.

## 14. Indicadores Operativos Recomendados

1. Total de estudiantes activos.
2. Total de secciones activas.
3. Total de asignaturas activas.
4. Porcentaje de actividades calificadas por asignatura.
5. Porcentaje de asistencia por seccion.
6. Tasa de aprobacion por asignatura.
7. Tasa de recuperacion por periodo.

## 15. Archivos Clave Del Sistema

1. `app.py`: inicializacion de la aplicacion y registro de blueprints.
2. `models.py`: modelo de dominio y persistencia.
3. `routes/*.py`: logica funcional por modulo.
4. `templates/**/*.html`: interfaz visual.
5. `static/js/app.js`: interacciones de navegacion.
6. `config.py`: configuracion principal.

## 16. Conclusión

TeacherApp cubre el ciclo operativo esencial del trabajo docente: planificar, matricular, evaluar, registrar asistencia y reportar. Su mayor fortaleza es la coherencia entre estructura academica, calificaciones y reportes en un entorno simple de desplegar y utilizable sin infraestructura compleja.
