import os
import json

from dotenv import load_dotenv
import google.generativeai as genai
import typing_extensions as typing

load_dotenv()


# スキーマオブジェクトの定義
class Recipe(typing.TypedDict):
    recipe_name: str


def main():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # モデルの準備
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro"
        # generation_config={"response_mime_type": "application/json"}
    )

    # プロンプトでJSON出力を指示
    # prompt = """次のJSONスキーマを使用して、サッカー選手の名前と年齢を答えて
    #
    # Recipe = {'recipe_name': int, 'age': int}
    # Return: list[Recipe]"""
    prompt = "NULLを返して。"

    # 制約付きデコードでJSON出力を指示
    result = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[Recipe]
        ),
        request_options={"timeout": 6000},  # タイムアウト
    )
    raw_response = result.text
    print(raw_response)

    # 文字列をJSONにパース
    response = []
    if raw_response is not None and len(raw_response) > 0:
        response = json.loads(raw_response)
        print(response)
    else:
        print("レスポンスが空です")

    # result.textをoutput.txtに追加する
    with open("result.txt", "a") as file:
        json.dump(response, file)
        file.write("\n")


if __name__ == "__main__":
    main()
