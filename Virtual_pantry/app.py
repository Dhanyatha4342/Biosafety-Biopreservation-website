from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pantry.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/get-items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM pantry_items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/get-expiring-items', methods=['GET'])
def get_expiring_items():
    today = datetime.now().date()
    expiring_soon = today + timedelta(days=7)
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM pantry_items WHERE expiration_date <= ?', (expiring_soon,)).fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/suggest-recipes', methods=['GET'])
def suggest_recipes():
    conn = get_db_connection()
    items = conn.execute('SELECT name FROM pantry_items').fetchall()
    conn.close()
    
    ingredients = [item['name'] for item in items]
    
    recipes = [
        {'name': 'Tomato Soup', 'ingredients': ['tomato', 'onion', 'garlic']},
        {'name': 'Vegetable Stir Fry', 'ingredients': ['bell pepper', 'carrot', 'soy sauce']}
    ]
    
    suggested_recipes = [recipe for recipe in recipes if set(recipe['ingredients']).issubset(set(ingredients))]
    
    return jsonify(suggested_recipes)

if __name__ == '__main__':
    app.run(debug=True)
