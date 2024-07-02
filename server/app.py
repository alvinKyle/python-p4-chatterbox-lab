from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == 'GET':
        message = Message.query.order_by(Message.created_at).all()
        return make_response([mess.to_dict() for mess in message],200 )
    
    elif request.method == 'POST':
        output = request.get_json()
        messo = Message(
            body = output['body'],
            username = output['username']
        )
        db.session.add(messo)
        db.session.commit()
        res = make_response(messo.to_dict(),201)
        return res
    

@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    messo = Message.query.filter_by(id=id).first()

    if request.method ==  'PATCH':
        output = request.get_json()
        for attr in output:
            setattr(messo,attr,output[attr])

        db.session.add(messo)
        db.session.commit()
        res = make_response(messo.to_dict(),200)
        return res
    
    elif request.method == 'DELETE':
        db.session.delete(messo)
        db.session.commit()

        res = make_response({'deleted':True},200)
        return res

if __name__ == '__main__':
    app.run(port=5555)
