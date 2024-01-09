"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, abort, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

# Update the database URI for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    cupcakes_data = [cupcake.to_dict() for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes_data)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        abort(404)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'], 
        size=data['size'], 
        rating=data['rating'], 
        image=data.get('image', DEFAULT_IMAGE))
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.to_dict()), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        abort(404)

    data = request.json
    for key, value in data.items():
        setattr(cupcake, key, value)

    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        abort(404)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

if __name__ == '__main__':
    app.run(debug=True)
