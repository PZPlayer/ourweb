import flask
from flask import request, jsonify, make_response
from data import db_session
from data.recipe import Recipes

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/news')
def get_news():
    db_sesion = db_session.create_session()
    recipes = db_sesion.query(Recipes).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'ingridients', 'content', 'user.name'))
                 for item in recipes]
        }
    )

@blueprint.route('/api/jobs')
def get_jobs():
    db_sesion = db_session.create_session()
    jobs = db_sesion.query(Recipes).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in jobs]
        }
    )

@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})
