from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint

if __name__ == "__main__":
    app = create_app()

    # Configuración Swagger
    SWAGGER_URL = "/docs"
    API_URL = "/static/swagger.yaml"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "API Chat"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



    app.run("0.0.0.0", 8080, debug=True)