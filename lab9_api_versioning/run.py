from app import create_app
from flasgger import Swagger

app = create_app()

# 1. Define the Swagger UI configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all rules
            "model_filter": lambda tag: True,  # all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

# 2. Define the security definitions for the "Authorize" button
template = {
    "swagger": "2.0",
    "info": {
        "title": "My Library API",
        "description": "API for managing books in a library",
        "version": "1.0"
    },
    "basePath": "/",
    "produces": [
        "application/json"
    ],
    # --- THIS IS THE IMPORTANT PART ---
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Token, typically 'Bearer <token>'. Enter just the token or 'Bearer <token>'."
        }
    }
    # -----------------------------------
}

# 3. Initialize Flasgger with the config and template
swagger = Swagger(app, config=swagger_config, template=template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)