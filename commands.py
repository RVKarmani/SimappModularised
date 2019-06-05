# coding: utf-8
__author__ = 'Rohit Vemparala'
__copyright = 'Copyright 2019, Rohit Vemparala'

from flask import current_app
from flask.cli import click, with_appcontext
from flask_security.utils import hash_password
from .models import db, Role, Project


@click.command('create-database')
@with_appcontext
def create_database():
    import string
    import random

    security = current_app.extensions.get('security')

    db.drop_all()
    db.create_all()

    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    analyst_role = Role(name='analyst')
    
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.add(analyst_role)
    db.session.commit()

    test_user = security.datastore.create_user(
        first_name='Admin',
        email='admin',
        password=hash_password('admin'),
        roles=[user_role, super_user_role]
    )
    db.session.commit()

    for _ in range(0, 100):
        _cost = random.randrange(1, 1000)
        _project = Project(
            name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
            cost=_cost
        )
        db.session.add(_project)

    db.session.commit()
