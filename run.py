from flask import Flask, request, render_template

app = Flask(__name__)


from tfidfpage import tfidf
app.register_blueprint(tfidf,url_prefix='/tfidf')
from sjetpage import sjet
app.register_blueprint(sjet,url_prefix='/sjet')
from simpage import sim
app.register_blueprint(sim,url_prefix='/sim')
if __name__ == '__main__':
    app.run()