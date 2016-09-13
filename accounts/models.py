from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Apelido / Usuario' , max_length=30, unique=True, validators = [
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido',
                'Este valor deve conter apenas letras, numeros e os caracteres: @/./+/-/_.',
                'invalid'
            )
        ], help_text="Um nome curto que será usado para identifica-lo de forma única na plataforma"
    )
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)
