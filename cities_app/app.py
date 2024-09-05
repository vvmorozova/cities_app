from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from geoalchemy2 import Geometry

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin1:admin@cities_app-db-1.cities_app_app-network:5432/cdn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    coordinates = db.Column(Geometry(geometry_type='POINT', srid=4326)) 

    def __repr__(self):
        return f'<City {self.name}>'

with app.app_context():
    db.create_all()

from geopy.geocoders import Nominatim
from geoalchemy2.shape import to_shape
from sqlalchemy import func

@app.route('/cities', methods=['POST'])
def add_city():
    
    data = request.json
    print(data)
    if not (('name') in data):
        return jsonify({'error': 'Missing data'}), 400
    
    name = data['name']

    geolocator = Nominatim(user_agent="CitiesApp")

    location = geolocator.geocode(name)
    coor = f'POINT({location.longitude} {location.latitude})'

    new_city = City(name=data['name'], coordinates=coor)

    try:
        db.session.add(new_city)
        db.session.commit()
        return jsonify({'message': 'City added successfully!', 'city': {'name': new_city.name, 'longitude': location.longitude, 'latitude': location.latitude}}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': f"City '{data['name']}' already exists."}), 409

@app.route('/cities', methods=['DELETE'])
def delete_city():
    data = request.json
    if not (('name') in data):
        return jsonify({'error': 'Missing data'}), 400
    
    name = data['name']
    city_to_delete = City.query.filter_by(name=name).first()
    
    if city_to_delete is None:
        return jsonify({'error': f'City with name {name} not found'}), 404

    db.session.delete(city_to_delete)
    db.session.commit()
    return jsonify({'message': 'City deleted successfully!'}), 200

@app.route('/cities', methods=['GET'])
def get_city_info():
    data = request.json
    if not (('name') in data):
        return jsonify({'error': 'Missing data'}), 400
    
    name = data['name']
    cities = City.query.filter_by(name=name)
    for city in cities:
        point = to_shape(city.coordinates)
        cities_list = {'name': city.name, 'longitude': point.x, 'latitude':point.y}
    return jsonify(cities_list), 200 

@app.route('/nearest_cities', methods=['GET'])
def get_nearest_city():
    data = request.json
    if not ((('longitude') and ('latitude'))in data):
        return jsonify({'error': 'Missing data'}), 400
    
    longitude = data['longitude']
    latitude = data['latitude']
    point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

    query = (
        db.session.query(
            City.name,
            func.ST_Distance(City.coordinates, point).label('distance')
        )
        .order_by('distance')
        .limit(2)
    )

    nearest_cities = query.all()
    
    answer = []
    for result in nearest_cities:
        answer.append({'name': result.name})
    return jsonify(answer), 200 
        
if __name__ == '__main__':
    app.run(debug=True)