from flask import Flask, request, jsonify, render_template, redirect, url_for
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
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        app.run(debug=True)