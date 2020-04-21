class Config(object):
    # Statement for enabling the development environment
    DEBUG = True
    ENV   = 'development'
    
    # Define the application directory
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

    UPLOAD_FOLDER = "application/static/uploads/"

    PROCESSING_FOLDER = "application/static/processing"

    APP_STATIC_FOLDER = "application/required_static_files"

    # Application threads
    THREADS_PER_PAGE = 2

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True

    # Use a secure, unique and absolutely secret key for
    # signing the data. 
    CSRF_SESSION_KEY = os.urandom(16)

    # Secret key for signing cookies
    SECRET_KEY = os.urandom(16)