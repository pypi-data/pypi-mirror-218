from threading import Thread
import datetime
import argparse
from .models import Models
import sys as _sys


class ListAction(argparse.Action):
    SUPPRESS = "==SUPPRESS=="

    def __init__(
        self,
        option_strings,
        version=None,
        dest=SUPPRESS,
        default=SUPPRESS,
        help="Show list of models",
    ):
        super(ListAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        models = Models().get_descriptions()
        parser._print_message("List of avaiable models:\n", _sys.stdout)
        for model in models:
            description = models[model]
            text = f" {model} - {description}\n"
            parser._print_message(text, _sys.stdout)

        parser.exit()


def read_command_line():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("source", type=str, help="source input file")

    parser.add_argument("target", type=str, help="output file")

    parser.add_argument("prompt", type=str, help="prompt to apply")

    parser.add_argument(
        "--model",
        type=str,
        choices=Models().get_choices(),
        default="gpt-3.5-turbo",
        help="model to use",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=8,
        help="Number of threads used for CPU inference",
    )

    parser.add_argument(
        "--models",
        action=ListAction,
    )

    d = parser.parse_args().__dict__
    return d["source"], d["target"], d["prompt"], d["model"], d["threads"]


def main():
    print("Large language models to text")
    source, target, prompt, model_name, threads = read_command_line()

    model = Models().get_model(model_name, prompt)
    n_threads = threads
    start_time = datetime.datetime.now()

    with open(source, "r") as in_file, open(target, "w") as tf_ca:
        en_strings = in_file.readlines()
        len_en_strings = len(en_strings)

        i = 0
        processed = 0
        while i < len_en_strings:
            threads = []
            sources = []
            translations = []
            num_threads = min(n_threads, len_en_strings - i)

            for t in range(0, num_threads):
                sources.append(en_strings[i + t].replace("\n", ""))
                translations.append("")

            for t in range(0, num_threads):
                process = Thread(
                    target=model.query_thread, args=[sources[t], translations, t]
                )
                process.start()
                threads.append(process)

            for process in threads:
                process.join()

            for t in range(0, num_threads):
                i = i + 1
                processed = processed + 1
                if processed % 1000 == 0:
                    print(processed)

                tgt = translations[t]
                tf_ca.write("{0}\n".format(tgt))

    print(f"Processed {processed} strings written to '{target}'")
    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))


if __name__ == "__main__":
    main()
