# porch_light

## Development setup
- Need Python > 3.10 Installed

- Install Go-Task
- Linux
  - sudo snap install task --classic;

## Python setup
```sh
task setup; task test;
```

## Secrets
**API keys are stored in env vars, plain and simple**
For local dev, these get loaded by `from dotenv import load_dotenv` from a PGP encrypted .env file. 
This file needs to be open during local testing. Hashi Vault would be nicer, but meh.
For docker builds, they get passed in via the task file (which reads the same .env file), which sets them on the host
For CI/CD, they are passed in via secrets from GitHub

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
