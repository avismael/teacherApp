from flask import Flask, render_template
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

    # Crear tablas
    with app.app_context():
        import models
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
