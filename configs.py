import os

APP_CONFIGS = {
    'PROPAGATE_EXCEPTIONS': True,
    'API_TITLE': 'Stores REST API',
    'API_VERSION': 'v1',
    'OPENAPI_VERSION': '3.0.3',
    'OPENAPI_URL_PREFIX': '/',
    'OPENAPI_SWAGGER_UI_PATH': '/swagger-ui',
    'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/',
    'SQLALCHEMY_DATABASE_URI': os.getenv("DATABASE_URL", 'sqlite:///data.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}

# print(APP_CONFIGS)