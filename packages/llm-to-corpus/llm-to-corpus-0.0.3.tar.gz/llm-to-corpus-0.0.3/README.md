[![PyPI version](https://img.shields.io/pypi/v/llm-to-corpus.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/llm-to-corpus/)

# Introduction

The goal of this tool is to apply Large Language Models operations to monolingual corpus to generate parallell corpus.

Uses cases:

* Asking a model to translate, summarize, paraphrasing original sentence to be able to benchmark its performance
* For corpus generation tasks from monolingual corpus, like for example, translated corpus.
* When developing prompts for your application, enables to test the prompt over a list of sentence to do evaluations

You basically provide an input file and prompt and it generates a target corpus:
![Alt text](docs/flow.svg?raw=true "Sample of the flow")

# Quick start

For example, to use OpenAI ChatGPT to translate a file:

```shell

llm-to-corpus samples/eng.txt samples/fra.txt "translate to French"
```

To see models and options available:
```shell

llm-to-corpus --help
```

# Usage

## Evaluation with Chatgpt

Translate Flores200 corpus to evalute quality of Catalan translation

```shell

llm-to-corpus samples/flores200.eng chatgpt.txt "Translate to Catalan the following text:"
```

```shell
pip install sacrebleu
```

```shell
sacrebleu samples/flores200.cat -i chatgpt.txt -m bleu chrf --format text
```



## Evaluation with Bloom

Translate Flores200 corpus to evalute quality of Catalan translation

```shell

llm-to-corpus samples/flores200.eng bloom.txt "Translate to Catalan the following text:" --model mt0-xxl-mt
```

```shell
pip install sacrebleu
```

```shell
sacrebleu samples/flores200.cat -i bloom.txt -m bleu chrf --format text
```



