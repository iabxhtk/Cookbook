from marshmallow import Schema, fields

from flask_cookbook.app import db


class RecipeModel(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    ingredients = db.relationship('RecipeIngredientModel', backref='recipe')


class UnitModel(db.Model):
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=True)

    @classmethod
    def find_by_desc(cls, description):
        return cls.query.filter_by(description=description).first()


class IngredientModel(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class RecipeIngredientModel(db.Model):
    __tablename__ = "recipes_ingredients"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    ingredient = db.relationship('IngredientModel')

    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=True)
    unit = db.relationship('UnitModel')

    quantity = db.Column(db.Numeric, nullable=False)


class IngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class UnitSchema(Schema):
    id = fields.Int()
    description = fields.Str()


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    quantity = fields.Number()
    unit = fields.Nested(UnitSchema(only=["description"]))
    ingredient = fields.Nested(IngredientSchema())


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    prep_time = fields.Int()
    ingredients = fields.Nested(RecipeIngredientSchema(many=True), data_key="list")


ingredients_schema = IngredientSchema(many=True)
detailed_recipes_schema = RecipeSchema(many=True)
recipes_list_schema = RecipeSchema(only=["name"])
