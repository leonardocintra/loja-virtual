# Loja Virtual (E-commerce)
Ecommerce - Django

[![Build Status](https://travis-ci.org/leonardocintra/loja-virtual.svg?branch=master)](https://travis-ci.org/leonardocintra/loja-virtual)

## Feito com Django 1.10
![image](https://cloud.githubusercontent.com/assets/5832193/17952257/3ee3156e-6a3f-11e6-8add-6eeccbf68e3c.png)

## Instalação
```
git clone https://github.com/leonardocintra/loja-virtual.git
virtualenv env -p python3
source enb/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Make a copy of `ecommerce/settings_local_example.py` into `ecommerce/settings_local.py` to configure your local settings.

## Watson
```
manage.py installwatson
```

**Existing website data:** If you're integrating django-watson with an existing site, then you'll also want to run `./manage.py buildwatson` to index your existing data.

Antes de executar o `buildwatson` precisa registrar as lib (ja esta resgistrada em catalog/apps.py)

[Duvidas leia a documentação](https://github.com/etianen/django-watson/wiki)

### Heroku Watson
```
python manage.py installwatson
python manage.py buildwatson
```


## Cache

Local and Heroku
```
python manage.py createcachetable
```


## Autor
Leonardo Nascimento Cintra - leonardo.ncintra@outlook.com
