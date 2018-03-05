import json

from flask import render_template, Flask, make_response, request, redirect, url_for, jsonify

from ..app.config import Config
from ..app.forms import ArticlesForm
from ..app.redis_handler import Category, Cat, N_ARTICLES, retrieve_item
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
    print(category)
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
        print(Category(category).articles)
        categories = {k.replace(str(Cat(category)) + ":", ""): v["_id"] for k, v in Category(category).articles.items()}
        return render_template('interface.html', form=form, category=category, categories=categories)


@app.route('/article_amazon/<amazon_id>')
def article_amazon(amazon_id):
    data = get_amazon_data_from_id(amazon_id)
    response_type = request.args.get("type", "json")
    if response_type == "json":
        return jsonify(data)
    elif response_type == "xml":
        template = render_template('template.xml', data=data)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response


@app.route('/tops/')
def get_top():
    list_data = []
    for cat in Cat:
        identifiant_produit = '{}:article{}'.format(cat, 1)
        data = {k: v for k, v in retrieve_item(identifiant_produit).items() if
                            k in ["_id", "image", "price", "title"]}
        if data:
            data["category"] = str(Cat(cat).value)

            list_data.append(data)

    return jsonify(list_data)


@app.route('/category/<category>')
def categorie(category):
    list_data = []
    if Cat.has_value(category):
        for i in range(N_ARTICLES):
            identifiant_produit = '{}:article{}'.format(Cat(category), i)
            data = {k: v for k, v in retrieve_item(identifiant_produit).items() if
                    k in ["_id", "image", "price", "title"]}
            if data :

                list_data.append(data)

    return jsonify(list_data)


@app.route('/article/<category>/<int:article_id>')
def article(category, article_id):
    if Cat.has_value(category) and article_id < N_ARTICLES:
        identifiant_produit = '{}:article{}'.format(Cat(category), article_id)
        data = retrieve_item(identifiant_produit)

        response_type = request.args.get("type", "json")

        if response_type == "json":
            return jsonify(data)
        elif response_type == "xml":
            template = render_template('template.xml', data=data)
            response = make_response(template)
            response.headers['Content-Type'] = 'application/xml'
            return response
