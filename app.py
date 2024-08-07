from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import ipython_config

def create_app():
    app = Flask(__name__)
    
    try:
        client = MongoClient(ipython_config.MONGO_URI)
        db = client.Cluster0
        collection = db.users
        print('Sucesso ao acessar o MongoDB!!')
    except Exception as e:
        print(f"Erro ao conctar ao MongoDB: {e}")
        return None
    
    @app.route('/')
    def home():
        try:
            items = list(collection.find())
            return render_template('index.html', items=items)
        except Exception as e:
            return jsonify({"error": f"Erro ao acessar a coleção: {e}"}), 500
    
    # Endpoint Read All [GET] /item
    @app.route('/item', methods=['GET'])
    def show_items():
        itens  = list(collection.find())
        
        for item in itens:
            item['_id'] = str(item['_id'])
        
        return jsonify(itens)
    
    # Endpoint Read By ID [GET] /item/<id>
    @app.route('/item/<id>', methods=['GET'])
    def show_item(id):
        try:
            item = collection.find_one({ "_id" : ObjectId(id)})
            item['_id'] = str(item['_id'])
            
            return jsonify(item)
        
        except Exception as e:
            return jsonify({"error": str(e)}),  404  
    
    # Endpoint Create [POST] criado
    @app.route('/item', methods=['POST'])
    def create_item():
        try:
            novo_item = request.json
        
            collection.insert_one(novo_item)
        
            if novo_item:
                novo_item['_id'] = str(novo_item['_id'])
        
            return jsonify(novo_item), 201
        
        except Exception as e:
            return jsonify({"error" : 'Body da requisição imcompleto'}), 400
        
    @app.route('/item/<id>', methods=['PUT'])
    def update_item(id):
        novo_item = request.json
        
        collection.update_one(
            { "_id" : ObjectId(id) },
            { "$set" : novo_item }
        )
        
        return jsonify(novo_item)
        
    @app.route('/item/<id>', methods=['DELETE'])
    def delete_item(id):        
        collection.delete_one({ '_id' : ObjectId(id) })
        
        return jsonify(f"Item deletado: {id}"), 200
        
        
    return app



if __name__ == '__main__':
    app = create_app()
    if app:
        app.run(debug=True)