from flask import Blueprint

BLUEPRINT = Blueprint('errors', __name__)

# It's imperative that this import comes after the blueprint definition.
from app.errors import handlers