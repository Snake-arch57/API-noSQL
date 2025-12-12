from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb+srv://<SEU USUÁRIO>:<dbpassword>@mongodb.xno9nzb.mongodb.net/SIEM?retryWrites=true&w=majority')
mongo = PyMongo(app)

CORS(app)


# LISTAR EVENTOS 
@app.route('/SIEM', methods=['GET'])
def listar_eventos():
    eventos = []
    for e in mongo.db.eventos.find():
        e['_id'] = str(e['_id'])     # converte para string
        eventos.append(e)
    return jsonify(eventos)



# INSERIR EVENTOS 
@app.route("/inserir_eventos", methods=['POST'])
def criar_eventos():
    data = request.json

    novo_evento = {
        "ip_origem": data.get("ip_origem"),
        "description": data.get("description"),
        "status": data.get("status", "OPEN"),
        "priority": data.get("priority", "LOW"),
        "created_at": datetime.datetime.utcnow(),
        "designado": data.get("designado", None)
    }

    mongo.db.eventos.insert_one(novo_evento)

    return jsonify({'success': True}), 201



# ATUALIZAR EVENTO
@app.route("/atualizar_eventos/<id>", methods=['PATCH'])
def atualizar_evento(id):

    data = request.json
    obj_id = ObjectId(id)

    result = mongo.db.eventos.update_one(
        {'_id': obj_id},
        {'$set': data}
    )

    return jsonify({
        "matched": result.matched_count,
        "modified": result.modified_count
    })



# DELETAR EVENTO
@app.route("/delete/<id>", methods=['DELETE'])
def deletar_evento(id):

    obj_id = ObjectId(id)
    result = mongo.db.eventos.delete_one({'_id': obj_id})

    return jsonify({"deleted": result.deleted_count})


app.run(debug=False, host='0.0.0.0', port=4444)


