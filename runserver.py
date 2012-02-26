from werkzeug import run_simple, DebuggedApplication
from application import application

run_simple('127.0.0.1', 8000, DebuggedApplication(application, True), use_reloader=True, use_debugger=True)
