from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_cookbook.app.core.cookbook_service import CookBookService

api = Namespace('cookbook', description='Used to manipulate cookbook recipes data.')

ingredient_api_model = api.model('Ingredient', {
    'name': fields.String(required=True, description="Name for the given ingredient")
})

recipe_ingredien_api_model = api.model('Recipe Ingredient', {
    'ingredient_id': fields.Integer(required=True, description="Ingredient's id"),
    'quantity': fields.Float(required=True, description="Ingredient measurement quantity"),
    'unit_id': fields.Integer(required=False, description="Optional measurement unit id"),
})

recipe_api_model = api.model('Recipe', {
    'name': fields.String(required=True, description="Name for the given recipe"),
    'description': fields.String(required=False, description="Name for the given recipe"),
    'prep_time': fields.Integer(required=False, description="Preparation time for the given recipe"),
    'ingredients': fields.List(fields.Nested(recipe_ingredien_api_model), description="Recipe's ingredients list",
                               required=True)
})


@api.route('/ingredients/<int:id>')
class Ingredient(Resource):
    @api.response(202, 'Ingredient successfully deleted.')
    @api.response(404, 'Ingredient with given id doesnt exist.')
    def delete(self, id):
        """Deletes an ingredient by given id."""
        return CookBookService.delete_ingredient_by_id(id)


@api.route('/ingredients/')
class IngredientsList(Resource):
    def get(self):
        """Retrieves all available ingredients."""
        return CookBookService.get_all_available_ingredients()

    @api.expect(ingredient_api_model, validate=True)
    @api.response(409, 'Ingredient with given name already exists.')
    @api.response(201, 'Ingredient successfully created.')
    def put(self):
        """Creates new ingredient entry"""
        return CookBookService.create_new_ingredient(request.json)


@api.route('/recipes/<int:id>')
@api.param('id', 'Recipe id.')
@api.response(404, 'Recipe with given id doesnt exist.')
class Recipe(Resource):
    def get(self, id):
        """Retrieves a recipe entry by given id."""
        return CookBookService.get_recipe_by_id(id)

    @api.response(202, 'Recipe successfully deleted.')
    def delete(self, id):
        """Deletes a recipe entry."""
        return CookBookService.delete_recipe_by_id(id)


@api.route('/recipes/')
class RecipeList(Resource):
    def get(self):
        """Retrieves recipes without the ingredients"""
        return CookBookService.get_all_recipes()

    @api.expect(recipe_api_model, validate=True)
    @api.response(409, 'The input data is wrong..')
    @api.response(201, 'Recipe successfully created.')
    def put(self):
        """Creates new recipe entry"""
        return CookBookService.create_new_recipe(request.json)


@api.route('/detailed_recipes/')
class DetailedRecipeList(Resource):
    def get(self):
        """Retrieves detailed recipe list with all it's informations and ingredients"""
        return CookBookService.get_all_detailed_recipes()


@api.route('/measurement_units/')
class MeasurementUnitList(Resource):
    def get(self):
        """Retrieves all available measurement units."""
        return CookBookService.get_all_measurement_units()
