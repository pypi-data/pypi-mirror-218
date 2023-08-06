import openai
import time
from threading import Thread
import datetime


class ChatGPT:
    def translate_thread(self, text, translations, index):
        #    print(f"translate_thread. Entry: {text}")
        while True:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    max_tokens=2000,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that paraphases text.",
                        },
                        {
                            "role": "user",
                            "content": f'Paraphase the following text in Catalan: "{text}"',
                        },
                    ],
                )
                break
            except Exception as error:
                print(f"error: {error}")
                time.sleep(30)

        translated = completion.choices[0].message["content"]
        if "\n" in translated or "\r" in translated:
            print(f"error line feed: {translated}")
            translated = text

        #    print(f"translate_thread. Translated: {translated}")
        translations[index] = translated
