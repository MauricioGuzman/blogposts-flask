SQLITE = "sqlite:///project.db"
POSTGRESQL = "postgresql+psycopg2://postgres:123456@localhost:5432/blogspots_db"


class Config:
    DEBUG = False #True
    SECRET_KEY =  'devBlog'  #'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL

    CKEDITOR_PKG_TYPE = 'full'