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
## Deploy
```sh 
task deploy
```

## Secrets
**API keys are stored in env vars, plain and simple**
```mermaid
flowchart

local_dev --env_file load via PyTest--> env_var
docker --env_file load via CLI--> env_var
gh_actions --Secrets--> env_var
env_var-->
api_key
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
