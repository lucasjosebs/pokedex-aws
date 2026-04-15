import requests
import pymysql


DB_HOST = 'seu-endpoint-rds-aqui'
DB_USER = 'seu-usuario-aqui'
DB_PASSWORD = 'sua-senha-aqui'
DB_NAME = 'seu-banco-de-dados-aqui'
BUCKET = 'seu-bucket-s3-aqui'
REGIAO = 'sua-regiao-aws-aqui'

# Quantos pokémons buscar (1 até 151 = geração 1, até 251 = geração 2)
TOTAL = 251

def conectar():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def buscar_pokemon(numero):
    url = f'https://pokeapi.co/api/v2/pokemon/{numero}'
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print(f'Erro ao buscar pokémon {numero}')
        return None
    return resposta.json()

def buscar_descricao(numero):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{numero}'
    resposta = requests.get(url)
    if resposta.status_code != 200:
        return 'Sem descrição disponível.'
    dados = resposta.json()
    for entry in dados['flavor_text_entries']:
        if entry['language']['name'] == 'en':
            texto = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            return texto
    return 'Sem descrição disponível.'

def traduzir_tipo(tipo_en):
    tipos = {
        'fire': 'Fogo',
        'water': 'Água',
        'grass': 'Planta',
        'electric': 'Elétrico',
        'psychic': 'Psíquico',
        'ice': 'Gelo',
        'dragon': 'Dragão',
        'dark': 'Sombrio',
        'fairy': 'Fada',
        'normal': 'Normal',
        'fighting': 'Lutador',
        'flying': 'Voador',
        'poison': 'Veneno',
        'ground': 'Terra',
        'rock': 'Pedra',
        'bug': 'Inseto',
        'ghost': 'Fantasma',
        'steel': 'Aço'
    }
    return tipos.get(tipo_en, tipo_en.capitalize())

def popular():
    conn = conectar()
    cursor = conn.cursor()
    inseridos = 0
    pulados = 0

    for numero in range(1, TOTAL + 1):
        print(f'Buscando pokémon {numero}/{TOTAL}...', end=' ')

        dados = buscar_pokemon(numero)
        if not dados:
            pulados += 1
            continue

        nome = dados['name'].capitalize()
        tipos = dados['types']
        tipo1 = traduzir_tipo(tipos[0]['type']['name'])
        tipo2 = traduzir_tipo(tipos[1]['type']['name']) if len(tipos) > 1 else None
        url_imagem = f'https://{BUCKET}.s3.{REGIAO}.amazonaws.com/{dados["name"]}.png'
        descricao = buscar_descricao(numero)

        try:
            cursor.execute("""
                INSERT INTO pokemon (numero, nome, tipo1, tipo2, url_imagem, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    nome = VALUES(nome),
                    tipo1 = VALUES(tipo1),
                    tipo2 = VALUES(tipo2),
                    url_imagem = VALUES(url_imagem),
                    descricao = VALUES(descricao)
            """, (numero, nome, tipo1, tipo2, url_imagem, descricao))
            conn.commit()
            print(f'OK — {nome}')
            inseridos += 1
        except Exception as e:
            print(f'ERRO — {e}')
            pulados += 1

    conn.close()
    print(f'\nConcluído! {inseridos} inseridos, {pulados} pulados.')

if __name__ == '__main__':
    popular()
