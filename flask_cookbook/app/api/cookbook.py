from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_cookbook.app.core.cookbook_service import CookBookService

api = Namespace('cookbook', description='Used to manipulate cookbook recipes data.')

ingredient_api_model = api.model('Ingredient', {
    'name': fields.String(required=True, description="Name for the given ingredient")
})


@api.route('/ingredients/<int:id>')
class Ingredient(Resource):
    def delete(self, id):
        """Deletes an ingredient by given id."""
        return CookBookService.delete_ingredient_by_id(id)


@api.route('/ingredients/')
class IngredientsList(Resource):
    def get(self):
        """Retrieves all available ingredients."""
        return CookBookService.get_all_available_ingredients()

    @api.expect(ingredient_api_model, validate=True)
    def put(self):
        """Creates new ingredient entry"""
        return CookBookService.create_new_ingredient(request.json)


@api.route('/recipes/<int:id>')
@api.param('id', 'Recipe id.')
@api.response(404, 'Recipe not found.')
class Recipe(Resource):
    def get(self, id):
        """Retrieves a recipe entry by given id."""
        return CookBookService.get_recipe_by_id(id)

    @api.response(204, 'Recipe deleted.')
    def delete(self, id):
        """Deletes a recipe entry."""
        pass

    def put(self):
        """Creates new recipe entry"""
        pass


@api.route('/recipes/')
class RecipeList(Resource):
    def get(self):
        return CookBookService.get_all_available_recipes()


@api.route('/detailed_recipes/')
class DetailedRecipeList(Resource):
    def get(self):
        """Retrieves detailed recipe list with all it's informations and ingredients"""
        return CookBookService.get_all_detailed_recipes()
