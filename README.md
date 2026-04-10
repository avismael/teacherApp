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

### 📊 Reportes y Análisis
- **Reporte por Estudiante:** Seguimiento individual del progreso y rendimiento académico.
- **Reporte por Asignatura:** Análisis grupal de resultados y promedios.
- **Exportación de Datos:** Capacidad para generar reportes profesionales y limpios.

### 🔒 Integridad y Seguridad
- **Borrado en Cascada:** Protección de integridad referencial para evitar inconsistencias en la base de datos.
- **Validaciones en Tiempo Real:** Asegura que los datos ingresados sean correctos y consistentes.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/)
- **Base de Datos:** [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite)
- **Frontend:** HTML5, CSS3 (Tailwind CSS) + Jinja2 Templates
- **Estilo:** Diseño premium con enfoque en la experiencia de usuario (UX).

---

## 📋 Requisitos Previos

- Python 3.8+
- Node.js (opcional, para compilación de CSS)
- Entorno virtual (recomendado)

---

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
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

## 📂 Estructura del Proyecto

```text
registro_notas/
├── routes/             # Lógica de rutas organizada por módulos
├── static/             # Archivos estáticos (CSS, JS, Imágenes)
├── templates/          # Plantillas Jinja2 (HTML)
├── app.py              # Punto de entrada de la aplicación
├── models.py           # Definición de modelos de base de datos
├── config.py           # Configuraciones globales
├── extensions.py       # Inicialización de extensiones (SQLAlchemy)
└── requirements.txt    # Dependencias del proyecto
```

---

## ✒️ Autor
Desarrollado con ❤️ para mejorar la gestión educativa.
