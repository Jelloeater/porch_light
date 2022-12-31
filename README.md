# porch_light

## Setup

```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

Module              | Packages
-|-
Code Formatting     | black, isort
Style enforcement   | flake8
Static types        | mypy
Git hooks           | pre-commit
Testing             | pytest, pytest-cov. pytest-pycharm

```text
 .
├──  .coveragerc               --> Coverage
├──  .dockerignore             --> Docker
├──  .editorconfig             --> Maintain consistent coding style
├──  .github
│  └──  workflows              --> GH Actions
├──  .gitignore
├──  .pre-commit-config.yaml   --> Pre Commit config
├──  Dockerfile
├──  Pipfile                   --> Requirements
├──  Pipfile.lock
├──  porch_light
│  ├──  __init__.py
│  └──  porch_light.py
├──  README.md
├──  setup.cfg                 --> Command defaults
└──  test
   ├──  __init__.py
   └──  test_porch_light.py
```
