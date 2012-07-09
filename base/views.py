from base import app
from site_configuration.themes import render

@app.route("/")
def front_page():
    return render('base.html')
