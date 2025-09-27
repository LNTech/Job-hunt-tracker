from app.blueprints.front import bp

@bp.route('/')
def index():
    return 'This is The Front End'