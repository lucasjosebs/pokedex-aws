from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# Configurações de conexão com o banco RDS
DB_HOST = 'seu-endpoint-aqui.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'sua-senha-aqui'
DB_NAME = 'pokedex'

def conectar():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/pokemon', methods=['GET'])
def listar_todos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon")
    resultado = cursor.fetchall()
    conn.close()
    return jsonify(resultado)

@app.route('/pokemon/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('q', '')
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        SELECT * FROM pokemon 
        WHERE nome LIKE %s 
        OR tipo1 LIKE %s 
        OR tipo2 LIKE %s 
        OR numero = %s
    """
    like = f'%{termo}%'
    numero = termo if termo.isdigit() else 0
    cursor.execute(sql, (like, like, like, numero))
    resultado = cursor.fetchall()
    conn.close()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)