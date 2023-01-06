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

When you run `task deploy` the following happens:
- The .env file gets decrypted
- Then it gets copied to the docker host,
- The container is started via the run task, which uses the .env to pass in the secrets 
- This is all ephemerial, if the container stops or the host is rebooted, the envs stored in the docker config are killed
- Yeah, you could SSH to the host and do a `docker inspect` on the container to get the creds, but the only thing more secure...
- ... would be to use Hashi Vault, maybe with rotating tokens... which is overkill.
- If someone has SSH access to a box, I have bigger problems...
- At least I don't have to worry about storing credentials, or could do a Github Actions deploy to spice it up.

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
