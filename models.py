import os
import datetime

from peewee import *

from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('padawans.sqlite')

  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer


class Padawan(UserMixin, Model):
    full_name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Course(Model):
    owner = ForeignKeyField(Padawan, backref='courses')
    title = CharField(unique=True)
    description = CharField(unique=True)
    start_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Enrollments(Model):
    course_id = ForeignKeyField(Course, backref='courses', on_delete='CASCADE') 
    padawan_id = ForeignKeyField(Padawan, backref='padawans')

    class Meta:
        database = DATABASE


def initialize():
    # connect to the database
    DATABASE.connect()
    DATABASE.create_tables([Padawan, Course, Enrollments], safe=True)
    print('THE TABLES HAVE BEEN CREATED!')
    DATABASE.close()
