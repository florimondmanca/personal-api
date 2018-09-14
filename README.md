# Personal API

[![Build Status](https://img.shields.io/travis-ci/florimondmanca/personal-api.svg?style=flat-square)](https://travis-ci.org/florimondmanca/personal-api)
[![Python](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg?style=flat-square)](https://www.djangoproject.com)
[![DigitalOcean](https://img.shields.io/badge/digitalocean-deployed-0069fe.svg?style=flat-square)](https://digitalocean.com)
[![CaptainDuckDuck](https://img.shields.io/badge/captainduckduck-quack-fdc73d.svg?style=flat-square)](https://captainduckduck.com)

[![](https://blog.florimondmanca.com/assets/img/codesail-full-repo.png)](https://blog.florimondmanca.com)

This is the repository for the **backend REST API** powering [CodeSail](https://blog.florimondmanca.com), my personal website and blog.

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

In production, user-uploaded files (such as images displayed in blog posts) are stored on an S3 bucket.

To configure S3 storage, provide the following environment variables:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME
```

For more information, see [Django Storages docs](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html).

## Deployment

Deployment is configured in `.travis.yml` and is powered by [CaptainDuckDuck](https://captainduckduck.com):

- After a successful CI build, a deployment to a server running on DigitalOcean is triggered.
- A Docker container defined in `captain-definition` is built from the `master` branch and run by CaptainDuckDuck on the host server.
- No further configuration is required on the host server, except setting the required environment variables as described in [Install](#install).
