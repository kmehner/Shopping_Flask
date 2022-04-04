from app import app
from app.blueprints.auth.models import User
from app.blueprints.cart.models import Item, CustomerCart

@app.shell_context_processor
def make_context():
    return {'User': User, 'Item': Item, 'CustomerCart':CustomerCart}