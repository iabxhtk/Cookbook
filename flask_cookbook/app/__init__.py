from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_cookbook.app.config import configurations
from flask_migrate import Migrate

from flask_cookbook.app.model import db
from flask_cookbook.app.api import api

b_crypt = Bcrypt()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(configurations[config_filename])

    b_crypt.init_app(app)
    api.init_app(app)
    db.init_app(app)

    jwt = JWTManager(app)
    # workaround...
    jwt._set_error_handler_callbacks(api)
    migrate = Migrate(app, db)
    from flask_cookbook.app.model.auth import UserModel, RevokedTokenModel
    from flask_cookbook.app.model.cookbook import UnitModel, IngredientModel, RecipeIngredientModel, RecipeModel

    @app.cli.command("create-data")
    def create_data():
        db.drop_all()
        db.create_all()
        db.session.commit()

        ingredients = [
            IngredientModel(name="Milk"),
            IngredientModel(name="Flour"),
            IngredientModel(name="Water"),
            IngredientModel(name="Salt"),
            IngredientModel(name="White sugar"),
            IngredientModel(name="Brown sugar"),
            IngredientModel(name="Butter"),
            IngredientModel(name="Egg"),
            IngredientModel(name="Baking powder"),
            IngredientModel(name="Heavy cream"),
            IngredientModel(name="Vanilla extract"),
            IngredientModel(name="Cookies"),
        ]
        db.session.bulk_save_objects(ingredients)

        units = [
            UnitModel(description="ml"),
            UnitModel(description="l"),
            UnitModel(description="oz"),
            UnitModel(description="tablespoon"),
            UnitModel(description="teaspoon"),
            UnitModel(description="cup"),
            UnitModel(description="g"),
            UnitModel(description="kg"),
        ]
        db.session.bulk_save_objects(units)

        icecream_ingredients = [
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Heavy cream"), quantity=2,
                                  unit=UnitModel.find_by_desc("cup")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Milk"), quantity=1.5,
                                  unit=UnitModel.find_by_desc("cup")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("White sugar"), quantity=1,
                                  unit=UnitModel.find_by_desc("cup")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Salt"), quantity=0.2,
                                  unit=UnitModel.find_by_desc("tablespoon")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Cookies"), quantity=2,
                                  unit=UnitModel.find_by_desc("cup")),
        ]

        icecream_recipe = RecipeModel(name="Ice Cream", description="How to make homemade Ice Cream in 5 minutes.",
                                      prep_time=5)
        icecream_recipe.ingredients.extend(icecream_ingredients)
        db.session.add(icecream_recipe)

        pancake_ingredients = [
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Flour"), quantity=1.5,
                                  unit=UnitModel.find_by_desc("cup")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Baking powder"), quantity=3.5,
                                  unit=UnitModel.find_by_desc("teaspoon")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Salt"), quantity=1,
                                  unit=UnitModel.find_by_desc("teaspoon")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("White sugar"), quantity=1,
                                  unit=UnitModel.find_by_desc("tablespoon")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Milk"), quantity=1.5,
                                  unit=UnitModel.find_by_desc("cup")),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Egg"), quantity=1),
            RecipeIngredientModel(ingredient=IngredientModel.find_by_name("Butter"), quantity=3,
                                  unit=UnitModel.find_by_desc("tablespoon")),
        ]

        pancakes_recipe = RecipeModel(name="Pancakes", description="How to make delicious pancakes", prep_time=15)
        pancakes_recipe.ingredients.extend(pancake_ingredients)
        db.session.add(pancakes_recipe)

        db.session.commit()

    return app
