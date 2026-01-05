import os
import requests
import random

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_japanese_name(data_list):
    """APIのリストから日本語の名前を探して返す"""
    for entry in data_list:
        if entry['language']['name'] == 'ja-Hrkt': # 読みやすい「ひらがな・カタカナ」を選択
            return entry['name']
    return "名前不明"

def main():
    # 1. ランダムなポケモンIDを選択 (1〜1010辺りまでが安定)
    pokemon_id = random.randint(1, 1010)
    
    # 2. 基本情報と詳細情報（種族情報）を両方取得
    base_res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    spec_res = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}")
    
    base_data = base_res.json()
    spec_data = spec_res.json()

    # --- 日本語データの抽出 ---
    # 名前
    jp_name = get_japanese_name(spec_data['names'])
    
    # 説明文（最新の図鑑説明を取得）
    description = ""
    for entry in spec_data['flavor_text_entries']:
        if entry['language']['name'] == 'ja': # 日本語の説明
            description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            break

    # タイプ（日本語変換用辞書）
    type_map = {
        'normal': 'ノーマル', 'fire': 'ほのお', 'water': 'みず', 'grass': 'くさ',
        'electric': 'でんき', 'ice': 'こおり', 'fighting': 'かくとう', 'poison': 'どく',
        'ground': 'じめん', 'flying': 'ひこう', 'psychic': 'エスパー', 'bug': 'むし',
        'rock': 'いわ', 'ghost': 'ゴースト', 'dragon': 'ドラゴン', 'dark': 'あく',
        'steel': 'はがね', 'fairy': 'フェアリー'
    }
    jp_types = [type_map.get(t['type']['name'], t['type']['name']) for t in base_data['types']]

    # 画像
    sprite = base_data['sprites']['front_default']

    # 3. Discordに送信
    payload = {
        "username": "ポケモン図鑑",
        "avatar_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png",
        "content": f"🍀 **今日のランダムポケモン**",
        "embeds": [{
            "title": f"No.{pokemon_id} : {jp_name}",
            "description": f"**タイプ:** {', '.join(jp_types)}\n\n**図鑑説明:**\n{description}",
            "image": {"url": sprite},
            "color": 16711680 # 赤色
        }]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    main()
