import os
import requests
import random

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def main():
    # 1. ランダムなポケモンIDを選択（第1世代〜最新付近まで）
    pokemon_id = random.randint(1, 1025)
    
    # 2. PokeAPIからデータを取得
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    data = response.json()
    
    name = data['name'].capitalize()
    sprite = data['sprites']['front_default']
    types = [t['type']['name'] for t in data['types']]

    # 3. Discordに送信する内容を作成
    payload = {
        "content": f"🍀 **今日のランダムポケモン**",
        "embeds": [{
            "title": f"No.{pokemon_id} : {name}",
            "description": f"タイプ: {', '.join(types)}",
            "image": {"url": sprite},
            "color": 16711680
        }]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    main()
