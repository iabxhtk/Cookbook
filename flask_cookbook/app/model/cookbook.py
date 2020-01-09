from flask_cookbook.app import db


class RecipeModel(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.relationship('RecipeIngredientModel', backref='recipe')
