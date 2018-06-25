# florimondmanca

This is the repository for my personal blog website, made with Django.

## Features

- Simple blogging system: create posts, let users react.
- No comments, no tags (told you — *it's simple*).
- Clean, minimal design for a graceful reader experience.

## Install

- Create a virtual environment and activate it

```bash
$ python3 -m venv env
$ source env/bin/activate
```

- Install dependencies

```bash
$ pip install -r requirements.txt
```

- Create a `.env` file with your `DATABASE_URL` pointing to a local database

- Run database migrations

```bash
$ python manage.py migrate
```

- Collect static files (WhiteNoise is used in production and in development).

```bash
$ python manage.py collectstatic
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
