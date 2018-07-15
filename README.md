# Personal API

[![Python](https://img.shields.io/badge/python-3.7-blue.svg)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg)](https://www.djangoproject.com)
[![Build Status](https://travis-ci.org/florimondmanca/personal-api.svg?branch=master)](https://travis-ci.org/florimondmanca/personal-api)
[![DigitalOcean](https://img.shields.io/badge/digitalocean-deployed-brightgreen.svg)](https://digitalocean.com)

This is the repository for the backend API powering Florimond Manca's personal website and his blog, CodeSail.

[See it live](http://www.florimondmanca.com)

## Features

Current:

- Simple blogging system:
  - Manage blog posts
  - Save posts as drafts and publish them later
  - No comments, no tags
- Secure API key and token authentication (ensure only the frontend app can request the API).

Coming soon:

- Medium-like user reactions

## Install

- Install dependencies using [Pipenv](https://docs.pipenv.org):

```bash
$ pipenv install
$ pipenv shell
```

- Create a `.env` file with the following contents:

```text
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

## Deployment

Deployment is configured in `.travis.yml` and is powered by [CaptainDuckDuck](https://captainduckduck.com):

- After a successful CI build, a deployment to a server running on DigitalOcean is triggered.
- A Docker container defined in `captain-definition` is built from the `master` branch and run by CaptainDuckDuck on the host server.
- No further configuration is required on the host server, except setting the required environment variables as described in [Install](#install)
