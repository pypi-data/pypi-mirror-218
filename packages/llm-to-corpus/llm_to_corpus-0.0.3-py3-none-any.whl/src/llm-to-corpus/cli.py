import time
from threading import Thread
import datetime
import argparse
from chatgpt import ChatGPT
import os

def read_command_line():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("source", type=str, help="source input file")

    parser.add_argument("target", type=str, help="output file")

    parser.add_argument("prompt", type=str, help="prompt to apply")

    parser.add_argument("--model", type=str, default="OpenAPI", help="model to apply")
    d = parser.parse_args().__dict__
    print(d)
    return d["source"], d["target"], d["prompt"], d["model"]


def main():
    source, target, prompt, model_name = read_command_line()
    
    if model_name == "OpenAPI":
        key = os.environ.get('OPENAI_API_KEY')
        if key is None or len(key) == 0:
            raise RuntimeError(f"You should set OPENAI_API_KEY environment variable with you OpenAI key")

    n_threads = 10
    start_time = datetime.datetime.now()
    model = ChatGPT()

    with open(source, "r") as in_file, open(target, "w") as tf_ca:
        en_strings = in_file.readlines()
        len_en_strings = len(en_strings)

        i = 0
        translated = 0
        while i < len_en_strings:
            threads = []
            sources = []
            translations = []
            num_threads = min(n_threads, len_en_strings - i)

            for t in range(0, num_threads):
                sources.append(en_strings[i + t].replace("\n", ""))
                translations.append("")

            for t in range(0, num_threads):
                src = sources[t]
                process = Thread(
                    target=model.translate_thread, args=[sources[t], translations, t]
                )
                process.start()
                threads.append(process)

            for process in threads:
                process.join()

            for t in range(0, num_threads):
                i = i + 1
                translated = translated + 1
                if translated % 1000 == 0:
                    print(translated)

                src = sources[t]
                tgt = translations[t]
                tf_ca.write("{0}\n".format(tgt))

    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))


if __name__ == "__main__":
    main()
