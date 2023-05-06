# Chess AI

## Getting started

### Prerequisites

You will need `pyhton3` and `git`. I would recommend `pyhton3.10` but others should work
too.

### Install

The following instructions are for linux. If you don't know how to apply them for your OS
(i.e. windows or mac), consider prompting ChatGPT to translate them to your OS.

```
git clone https://github.com/PraxTube/chess-ai.git
cd chess-ai
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

if everything went well, you should be able to run the project with

```
pyhton src/chess_ai/main.py
```

## Contributing

### Set up

In order to contribute to this repo, you will need to set up and SSH key for you github
account. You can follow these steps
[here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
Note that you will want to change your `git remote origin` in your `chess-ai` folder. If
you don't know how to do this, then you can simply run
`git clone git@github.com:PraxTube/chess-ai.git` and then follow the steps above to set it
up.

### Conventions

We are using [black](https://github.com/psf/black) and [flake8](https://github.com/PyCQA/flake8)
to format our python code. You can run the following commands when you are in you venv

```
black .
flake8 .
```

The first one will automatically format you code in-place. If you prefer to see
if it would change anything, you can use the flag `--check`.

## Milestone I - Dummy AI

The deadline for this is the **11th Mai**.

### Coding TODO's

- \[x\] Code Framework
- \[x\] Move Generator
- \[x\] Evaluation function
- \[x\] Time Management
- \[x\] Pick move
- \[ \] Unit tests
- \[ \] Benchmarks

### Documentation TODO's

- \[ \] Class diagram
- \[ \] Plots of benchmarks
- \[ \] Future plans
- \[ \] Screencast
