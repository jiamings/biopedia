from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/<language>/index')
def index(language='en'):
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template.
    """
    return render_template('index.html', language=language)

# TODO: projects, profiles, data


if __name__ == '__main__':
    app.run(debug=True)
