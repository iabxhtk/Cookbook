from flask_cookbook.app.model.cookbook import IngredientModel, ingredients_schema, detailed_recipes_schema, RecipeModel, \
    recipes_list_schema


class CookBookService:
    @staticmethod
    def get_all_available_ingredients():
        data = IngredientModel.query.all()
        return {'ingredients': ingredients_schema.dump(data)}

    @staticmethod
    def get_all_available_recipes():
        data = RecipeModel.query.all()
        return {'ingredients': recipes_list_schema.dump(data)}

    @staticmethod
    def get_all_detailed_recipes():
        data = RecipeModel.query.all()
        return {'ingredients': detailed_recipes_schema.dump(data)}
