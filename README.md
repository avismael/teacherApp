# 🎓 TeacherApp - Sistema de Registro de Notas

Un sistema profesional y robusto diseñado para la gestión académica, permitiendo a los docentes llevar un control detallado de estudiantes, asignaturas, evaluaciones y calificaciones con integridad de datos garantizada.

---

## 🚀 Características Principales

### 📚 Gestión Académica
- **Asignaturas y Secciones:** Organización modular de materias y grupos de estudiantes.
- **Periodos Flexibles:** Definición de periodos académicos personalizados por asignatura.
- **Actividades con Ponderación:** Creación de actividades evaluativas con porcentajes específicos que suman el 100% de la nota del periodo.

### ✍️ Control de Calificaciones
- **Registro de Notas:** Interfaz intuitiva para ingresar calificaciones por actividad.
- **Rúbricas Detalladas:** Sistema integrado de evaluación basado en criterios y niveles de desempeño.
- **Notas de Recuperación:** Soporte para procesos de refuerzo académico por periodo.

### 📅 Control de Asistencia
- **Registro Rápido:** Toma de asistencia (Presente, Ausente, Tarde, Permiso) con interfaz optimizada para móviles (scroll horizontal en tablas).
- **Reportes de Asistencia:** Visualización de porcentajes e historial de asistencia por estudiante en las secciones y periodos.

### 📊 Reportes y Análisis
- **Reporte por Estudiante:** Seguimiento individual del progreso y rendimiento académico.
- **Reporte por Asignatura:** Análisis grupal de resultados y promedios.
- **Exportación de Datos:** Capacidad para generar reportes profesionales y limpios.

### 🔒 Integridad y Disponibilidad
- **Borrado en Cascada:** Protección de integridad referencial para evitar inconsistencias en la base de datos.
- **Validaciones en Tiempo Real:** Asegura que los datos ingresados sean correctos y consistentes.
- **100% Offline:** Assets (CSS nativo, fuentes web) previamente localizados, garantizando una funcionalidad completa y de alta velocidad sin conexión a internet.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/)
- **Base de Datos:** [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite)
- **Frontend:** HTML5, CSS3 (Tailwind CSS) + Jinja2 Templates
- **Estilo:** Diseño premium con enfoque en la experiencia de usuario (UX).

---

## 📋 Requisitos Previos

- Python 3.8+
- Node.js (opcional, solo si deseas modificar y compilar los estilos de Tailwind CSS)
- Entorno virtual (recomendado)

---

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [url-del-repositorio>](https://github.com/avismael/teacherApp.gi)
   cd registro_notas
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar dependencias de Frontend (si es necesario):**
   ```bash
   npm install
   ```

---

## 🏃 Cómo Ejecutar

### Modo Desarrollo
Para iniciar la aplicación localmente:
```bash
python app.py
```
La aplicación estará disponible en `http://localhost:5000`.

### Scripts de Utilidad
- `registro_notas.bat`: Script de inicio rápido para Windows.
- `build_css.bat`: Script para compilar los estilos de Tailwind CSS.

---

## 📥 Estructuras de Importación (CSV)

Para asegurar una importación masiva correcta, los archivos CSV deben seguir las estructuras detalladas a continuación. Se recomienda usar codificación **UTF-8**.

### 1. Importación de Estudiantes
Se utiliza en el módulo de Estudiantes para registrar alumnos de forma masiva.
- **Columnas Requeridas:** `NIE`, `Nombres`, `Apellidos`, `Género`
- **Formato:**
  ```csv
  NIE,Nombres,Apellidos,Género
  12345678,Juan Pérez,García,Masculino
  87654321,María López,Rodríguez,Femenino
  ```
- **Notas:** El sistema omitirá automáticamente la primera fila si detecta que contiene encabezados.

### 2. Importación de Rúbricas
Se utiliza dentro de la configuración de una Actividad para definir los criterios de evaluación.
- **Columnas Requeridas:** `Criterio`, `Nivel`, `Puntos`, `Descripción`
- **Formato:**
  ```csv
  Criterio,Nivel,Puntos,Descripcion
  Ortografía,Excelente,2.0,Sin errores ortográficos.
  Ortografía,Regular,1.0,Menos de 3 errores.
  Contenido,Bueno,5.0,Desarrolla todos los puntos.
  ```
- **Notas:** 
  - El sistema agrupa los niveles bajo el mismo nombre de criterio.
  - Los puntos aceptan decimales (ej. `0.5` o `1.0`).
  - La descripción es opcional pero recomendada para mayor claridad.

---

## 📂 Estructura del Proyecto

```text
registro_notas/
├── routes/             # Módulos de rutas (asistencia, calificaciones, evaluaciones, etc.)
├── static/             # Archivos estáticos (CSS, JS, Fuentes, Imágenes) para uso offline
├── templates/          # Plantillas Jinja2 (HTML)
├── app.py              # Punto de entrada de la aplicación
├── models.py           # Modelos de bases de datos
├── config.py           # Configuraciones globales de la app
├── extensions.py       # Inicialización de extensiones
└── requirements.txt    # Dependencias de Python
```

---

## ✒️ Autor
Desarrollado con ❤️ para mejorar la gestión educativa.
