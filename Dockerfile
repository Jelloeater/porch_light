FROM python:3.10-slim AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps
# Set timezone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc git
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN pipx install poetry
# Install python dependencies
COPY pyproject.toml .
COPY poetry.lock .
# RUN poetry install

FROM python-deps AS runtime

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
# Don't forget to check the .dockerignore
COPY . .

# Run the executable
RUN ls -a -R
CMD [ "python", "pl_worker/porch_light.py" ]
