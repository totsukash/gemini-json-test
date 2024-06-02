import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def main():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # モデルの準備
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )

    # プロンプトでJSON出力を指示
    prompt = """次のJSONスキーマを使用して、サッカー選手の名前と年齢を答えて

    Recipe = {'recipe_name': int}
    Return: list[Recipe]"""

    # 推論実行
    raw_response = model.generate_content(prompt)
    print("raw_response: ", raw_response.text)

    # 文字列をJSONにパース
    if raw_response is not None and len(raw_response.text) > 0:
        response = json.loads(raw_response.text)
        print(response)
    else:
        print("レスポンスが空です")


if __name__ == "__main__":
    main()
