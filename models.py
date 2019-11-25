import datetime

from peewee import *

from flask_login import UserMixin

DATABASE = SqliteDatabase('padawans.sqlite')


class Padawan(UserMixin, Model):
    full_name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Course(Model):
    owner = ForeignKeyField(Padawan, backref='courses')
    title = CharField(unique=True)
    description = CharField()
    start_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Enrollments(Model):
    course_id = ForeignKeyField(Course, backref='courses')
    padawan_id = ForeignKeyField(Padawan, backref='padawans')

    class Meta:
        database = DATABASE


def initialize():
    # connect to the database
    DATABASE.connect()
    DATABASE.create_tables([Padawan, Course, Enrollments], safe=True)
    print('THE TABLES HAVE BEEN CREATED!')
    DATABASE.close()
