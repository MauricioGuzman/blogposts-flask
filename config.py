#import os
SQLITE = "sqlite:///project.db"
POSTGRESQL = "postgresql+psycopg2://postgres:123456@localhost:5432/blogspots_db"
#USERNAME = 'super'  # Obtén tu nombre de usuario de PythonAnywhere
#PASSWORD = 'Python$123.'  # Define y obtén tu contraseña de la base de datos
#POSTGRESQL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@HectorGuzman-4515.postgres.pythonanywhere-services.com:14515/blogspots_db"


class Config:
    DEBUG = False #True
    SECRET_KEY =  'devBlog'  #'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL

    CKEDITOR_PKG_TYPE = 'full'





