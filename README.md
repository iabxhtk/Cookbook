# Running the application:

- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- export FLASK_APP=run
- export FLASK_ENV=development
- flask db migrate
- flask db upgrade
- flask run

App should be running at http://127.0.0.1:5000/

# Using the api:
The api was implemented with swagger ui documentation. You can play arround with API throguh the interactive documentation or consume the api any other way.

# Sending authentication jwt:
The jwt must be included in the requests header as:
>"Authentication: $ACCESS_TOKEN"

Example:
>curl -H "Authorization: $ACCESS_TOKEN"  http://127.0.0.1:5000/auth/token_check

# Available endpoints:
### Auth:
- **POST /auth/signin**  - logs in the user and retrieves the jwt access token.
- **POST /auth/signup** - creates new user.
- **GET /auth/token_check** - checks if access token is still valid.
- **GET /auth/user** - fetches all registered users.

### Cookbook:
All cookbook endpoints require a valid jwt.
- **GET /cookbook/detailed_recipes/** - Retrieves detailed recipe list with all it's informations and ingredients.
- **PUT /cookbook/ingredients/** - Creates new ingredient entry
- **GET /cookbook/ingredients/** - Retrieves all available ingredients
- **DELETE /cookbook/ingredients/{id}** - Deletes an ingredient by given id
- **GET /cookbook/measurement_units/** - Retrieves all available measurement units
- **PUT /cookbook/recipes/** - Creates new recipe entry
- **GET /cookbook/recipes/ **- Retrieves recipes without the ingredients
- **GET /cookbook/recipes/{id}** - Retrieves a recipe entry by given id
- **DELETE /cookbook/recipes/{id}** - Deletes a recipe entry


# TODO:
- get rid of marshamallow and Flask-Restplus models mix.
- implement recipes filtering
- refactor the code
