from flask import render_template, Flask, make_response, request, redirect, url_for, jsonify

from kadrop_api.app.config import Config
from kadrop_api.app.forms import ArticlesForm
from kadrop_api.app.redis_handler import Category, Cat, N_ARTICLES, get_key
from ..amazon_extractor import get_amazon_data_from_id

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return "<h1>KaDrop API</h1>"


@app.route('/interfaces')
def interfaces():
    return "<h1>Interfaces</h1>"


@app.route('/interface/<category>', methods=['GET', 'POST'])
def interface(category):
    form = ArticlesForm(request.form)

    if not Cat.has_value(category.lower()):
        return redirect(url_for('interfaces'))
    else:
        if request.method == 'POST' and form.validate_on_submit():
            categ = Category(category=category, list_of_article={
                "article1": form.article1.data,
                "article2": form.article2.data,
                "article3": form.article3.data,
                "article4": form.article4.data,
                "article5": form.article5.data,
                "article6": form.article6.data
            })
            return redirect(url_for('interfaces'))
        categories = {k.replace(str(Cat(category)) + ":", ""): v for k, v in Category(category).articles.items()}
        return render_template('interface.html', form=form, category=category, categories=categories)


@app.route('/article_amazon/<amazon_id>.xml')
def article_amazon(amazon_id):
    data = get_amazon_data_from_id(amazon_id)
    template = render_template('template.xml', data=data)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/nique_ta_mere')
def nique_ta_mere():
    data = get_amazon_data_from_id("B01KHFIVIU")
    return jsonify(data)


@app.route('/article/<category>/<int:article_id>.xml')
def article(category, article_id):
    if Cat.has_value(category) and article_id < N_ARTICLES:
        identifiant_produit = '{}:article{}'.format(Cat(category),article_id )
        amazon_id = get_key(identifiant_produit)
        data = get_amazon_data_from_id(amazon_id)
        template = render_template('template.xml', data=data)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
