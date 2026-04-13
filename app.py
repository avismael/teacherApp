from flask import Flask, render_template
import os
from config import Config
from extensions import db

# blueprints
from routes.dashboard import dashboard_bp
from routes.asignaturas import asignaturas_bp
from routes.secciones import secciones_bp
from routes.estudiantes import estudiantes_bp
from routes.evaluaciones import evaluaciones_bp
from routes.calificaciones import calificaciones_bp
from routes.reportes import reportes_bp
from routes.asistencia import asistencia_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registro de Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(asignaturas_bp, url_prefix='/asignaturas')
    app.register_blueprint(secciones_bp, url_prefix='/secciones')
    app.register_blueprint(estudiantes_bp, url_prefix='/estudiantes')
    app.register_blueprint(evaluaciones_bp, url_prefix='/evaluaciones')
    app.register_blueprint(calificaciones_bp, url_prefix='/calificaciones')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(asistencia_bp, url_prefix='/asistencia')

    # Crear tablas
    with app.app_context():
        import models
        db.create_all()
        
        # Asegurar directorios de subida
        if not os.path.exists(app.config['UPLOAD_FOLDER_ASISTENCIA']):
            os.makedirs(app.config['UPLOAD_FOLDER_ASISTENCIA'], exist_ok=True)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
