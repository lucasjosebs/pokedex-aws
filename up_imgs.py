import requests
import boto3

BUCKET_NAME = 'seu-bucket-s3-aqui'
START_ID = 1
END_ID = 251

s3_client = boto3.client('s3')

def download_and_upload_by_name():
    print(f"Iniciando processamento dos IDs {START_ID} a {END_ID}...")

    for poke_id in range(START_ID, END_ID + 1):
        try:
            api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
            pokemon_data = requests.get(api_url).json()
            pokemon_name = pokemon_data['name'] 
            
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{poke_id}.png"
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                file_name = f"{pokemon_name}.png"
                
                s3_client.put_object(
                    Bucket='seu-bucket-s3-aqui',
                    Key=file_name,
                    Body=image_response.content,
                    ContentType='image/png'
                )
                print(f"✅ [{poke_id}] {file_name} enviado com sucesso!")
            else:
                print(f"⚠️ [{poke_id}] Imagem não encontrada para {pokemon_name}")

        except Exception as e:
            print(f"❌ Erro no ID {poke_id}: {str(e)}")

if __name__ == "__main__":
    download_and_upload_by_name()
