# Flask example

Using Flask to build a Restful API Server.

Integration with Flask-restful, Flask-SQLalchemy.

### Extension:

- Restful: [Flask-restplus](http://flask-restplus.readthedocs.io/en/stable/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure

```
.
|──────app/
| |────models
| | |────__init__.py
| | |────user_model.py
| |
| |
| |────ressources
| | |────__init__.py
| | |────token_ressource.py
| | |────user_ressource.py
| |
| |──────app.py
| |──────blocklist.py
| |──────constant.py
| |──────db.py
| |──────README.md
| |──────requirements.txt
| |
|

```

## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```

### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

```

##Flask settings
DEBUG = True  # True/False
....


```

## Run Flask

### Run flask for develop

```
$ python Gladys_anoh-back/app.py
```

In flask, Default port is `5000`

Principal ressource endpoint: `http://127.0.0.1:5000/api`

### Run flask for production

** Run with gunicorn **

In Gladys_anoh-back/

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

- -w : number of worker
- -b : Socket to bind

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restful](http://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [gunicorn](http://gunicorn.org/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)

[Wiki Page](https://github.com/tsungtwu/flask-example/wiki)

## Changelog

- Version 2.0 : add SQL ORM extension: FLASK-SQLAlchemy
- Version 1.1 : update nosetest
- Version 1.0 : basic flask-api with Flask-Restful, Flask-jwt-extended
