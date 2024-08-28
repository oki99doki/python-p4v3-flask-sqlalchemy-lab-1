# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

# instance of api
app = Flask(__name__)

# config during init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add routes here

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    q = Earthquake.query.filter_by(id=id).first()

    if (not q):
        return {'message': f'Earthquake {id} not found.'}, 404
    
    return jsonify(q.to_dict()), 200


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_mag(magnitude):
    q = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    q_dict = [quake.to_dict() for quake in q]
    ret_json = {
        "count": len(q_dict),
        "quakes": q_dict
        }
    return jsonify(ret_json), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
