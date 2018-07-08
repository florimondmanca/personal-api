# FlorimondManca API

This is the repository for the backend API powering Florimond Manca's personal website and his blog, CodeSail.

<p class="text-center">
  <a href="#">See it live</a>
</p>

## Features

- Simple blogging system:
  - Manage blog posts
  - No comments, no tags
- Medium-like user reactions
- Secure API key and token authentication (ensure only the frontend app can request the API).

## Install

- Install dependencies using Pipenv:

```bash
$ pipenv install
$ pipenv shell
```

- Create a `.env` file with the following contents:

```text
# URL pointing to your local database
DATABASE_URL=...
DEBUG=True

# optional but required to run via Procfile (e.g. using `heroku local`)
HOST=localhost
PORT=8000
```

- Run database migrations

```bash
$ python manage.py migrate
```

## Quick start

You can:

- Run the development server

```bash
$ python manage.py runserver
```

- Run the tests

```bash
$ python manage.py test
```

## Deployment

This application can be readily deployed on Heroku.
