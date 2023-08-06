# "mathactive"

<!--
[![PyPI version](https://img.shields.io/pypi/pyversions/mathactive.svg)](https://pypi.or
g/project/mathactive/)
[![License](https://img.shields.io/pypi/l/mathactive.svg)](https://pypi.python.org/pypi/
mathactive/)
[![codecov](https://codecov.io/gl/tangibleai/mathactive/branch/master/graph/badge.svg)](
https://codecov.io/gl/tangibleai/mathactive)
[![Buy Us Tea](https://github.com/nlpia/nlpia-bot/raw/develop/docs/media/small-lea
f-and-name-screenshot-31x80.png)](https://buymeacoffee.com/hobs)
[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/
WWW/Badge%202.svg)](https://www.digitalocean.com/?refcode=5bc34fba1bee&utm_campaig
n=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
 -->
Conversational math active learning.

K-12 student can learn math from a chatbot that helps them actively solve math problems suitable to their skill level.

## Quickstart

If you have install python packages from source before, you will probably be able to follow these steps to get going quickly:

```bash
pip install --upgrade pip virtualenv poetry
git clone git@gitlab.com:tangbileai/community/mathactive
cd mathactive
python -m virtualenv .venv
source .venv/bin/activate || source .venv/Scripts/activate
pip install --editable .
```

## Utilities

```python
def get_countq_start_step(difficulty=0.01):
    """ Predict the parameters of a quiz question generator based on the desired difficulty
    >>> get_start_step(difficulty=.02)
    {'start': 0, 'step': 1}
    >>> get_start_step(difficulty=.03)
    {'start': 0, 'step': 1}
    >>> get_start_step(difficulty=.04)
    {'start': 10, 'step': 1}
    """
```

## Directory structure

```text
├── docs
│   ├── AIMA approaches to creating a chatbot.md
│   ├── ...
├── pyproject.toml
├── README.md
├── scripts
│   ├── bump_version.py
│   ├── release.sh
│   └── requirements.txt
└── src
    └── mathactive
        ├── data
        │   └── difficulty_start_stop_step.csv
        ├── data.csv
        ├── db.sqlite3
        ├── generators.py
        ├── hints.py
        ├── machine.py
        ├── manage.py
        ├── microlessons
        │   ├── num_one.py
        │   └── utils.py
        ├── personalize.py
        ├── python_quiz.py
        ├── questions.py
        ├── utils.py
        ├── webapp
        │   ├── admin.py
        │   ├── apps.py
        │   ├── migrations
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        └── website
            ├── asgi.py
            ├── settings.py
            ├── urls.py
            └── wsgi.py
```
