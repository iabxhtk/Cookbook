from marshmallow import Schema, fields

from flask_cookbook.app import db
from flask_cookbook.app.model.cookbook import IngredientModel, RecipeModel, RecipeIngredientModel, UnitModel


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
recipes_list_schema = RecipeSchema(many=True, exclude=["ingredients"])
units_schema = UnitSchema(many=True)


class CookBookService:
    @staticmethod
    def create_new_ingredient(data):
        name = data["name"]
        ingredient = IngredientModel.find_by_name(name)
        if ingredient is not None:
            return {"error": "Ingredient with given name already exists."}, 409
        ingredient = IngredientModel(name=name)
        db.session.add(ingredient)
        db.session.commit()
        return None, 201

    @staticmethod
    def delete_ingredient_by_id(ingredient_id):
        ingredient = IngredientModel.query.filter_by(id=ingredient_id).first()
        if ingredient is None:
            return {"error": "Ingredient with given id doesn't exist."}, 404

        db.session.delete(ingredient)
        db.session.commit()
        return None, 202

    @staticmethod
    def get_all_available_ingredients():
        data = IngredientModel.query.all()
        return ingredients_schema.dump(data)

    @staticmethod
    def get_recipe_by_id(recipe_id):
        data = RecipeModel.query.filter_by(id=recipe_id).first()
        if not data:
            return None, 404
        return recipes_list_schema.dump(data)

    @staticmethod
    def delete_recipe_by_id(recipe_id):
        recipe = RecipeModel.query.filter_by(id=recipe_id).first()
        if recipe is None:
            return {"error": "Recipe with given id doesn't exist."}, 404

        db.session.delete(recipe)
        db.session.commit()
        return None, 202

    @staticmethod
    def create_new_recipe(data):
        recipe_ingredients = []
        for ingredient_data in data["ingredients"]:
            recipe_ingredient_model = RecipeIngredientModel(unit_id=ingredient_data.get("unit_id", None),
                                                            ingredient_id=ingredient_data["ingredient_id"],
                                                            quantity=ingredient_data["quantity"])
            recipe_ingredients.append(recipe_ingredient_model)
        recipe_model = RecipeModel(ingredients=recipe_ingredients, name=data["name"], description=data["description"],
                                   prep_time=data["prep_time"])
        try:
            db.session.add(recipe_model)
            db.session.commit()
            return None, 201
        except Exception as e:
            return {"error": e}, 409

    @staticmethod
    def get_all_recipes():
        data = RecipeModel.query.all()
        return recipes_list_schema.dump(data)

    @staticmethod
    def get_all_detailed_recipes():
        data = RecipeModel.query.all()
        return detailed_recipes_schema.dump(data)

    @staticmethod
    def get_all_measurement_units():
        data = UnitModel.query.all()
        return units_schema.dump(data)
