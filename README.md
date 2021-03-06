# NOTICE

Now unused. See [florimondmanca/www](https://github.com/florimondmanca/www).

---

# Personal API

[![Build Status](https://img.shields.io/travis/florimondmanca/personal-api.svg?style=flat)](https://travis-ci.org/florimondmanca/personal-api)
[![Python](https://img.shields.io/badge/python-3.7-blue.svg?style=flat)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg?style=flat)](https://www.djangoproject.com)
[![DigitalOcean](https://img.shields.io/badge/digitalocean-deployed-0069fe.svg?style=flat)](https://digitalocean.com)
[![Dokku](https://img.shields.io/badge/platform-dokku-fdc73d.svg?style=flat)](http://dokku.viewdocs.io/dokku/)

This is the repository for the **backend REST API** powering my [blog](https://blog.florimond.dev).

## Features

Current:

- Manage blog posts
- Save posts as drafts and publish them later
- Simple tagging system
- RSS feed
- No comment system (yet?)
- Secure API key and token authentication (ensure only the frontend app can request the API).

## Install

- Install dependencies using [Pipenv](https://docs.pipenv.org):

```bash
$ pipenv install
$ pipenv shell
```

- Create a `.env` file with the following contents:

```
# Django secret key
SECRET_KEY=...
# URL pointing to your local database
DATABASE_URL=...
# Should not be set in production, only for local development
DEBUG=True
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

## CI/CD

Travis CI is configured on this repo and will run the test suite on every push to a branch.

## Media storage

In production, user-uploaded files (such as images displayed in blog posts) are stored in an S3 bucket.

To configure S3 storage, provide the following environment variables:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME
```

For more information, see [Django Storages docs](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html).

### About Pipenv

Although Pipenv can be used for local development, my single-core, 1GB RAM virtual machine couldn't handle `pipenv install`'s high CPU and RAM load.

As a workaround, I use a generated `requirements.txt` file.

Make sure to re-run `pipenv lock -r > requirements.txt` anytime dependencies are updated.
