from flask import Flask, render_template
from backend.routes.route import routes

# create the flask app
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.register_blueprint(routes)


# @app.route('/')
# def index():
#     #render the index.html file
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
