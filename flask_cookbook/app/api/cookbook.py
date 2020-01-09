from flask_restplus import Namespace, Resource

from flask_cookbook.app.core.cookbook_service import CookBookService

api = Namespace('cookbook', description='Used to retrieve cookbook recipes data.')


@api.route('/ingredients/')
class IngredientsList(Resource):
    def get(self):
        return CookBookService.get_all_available_ingredients()


@api.route('/recipes/')
class RecipesList(Resource):
    def get(self):
        return CookBookService.get_all_available_recipes()


@api.route('/detailed_recipes/')
class DetailedRecipes(Resource):
    def get(self):
        return CookBookService.get_all_available_recipes()
