# User Story

- the first person who registers with the username 'admin' will have the admin rights
- every other user will be a padawan

1. user will be brought to the homepage
2. user will register if they do not have an account next
3. user will to select their courses -- a minimum of 3
4. if user has an account they will be brought to the landing page

   ## If user is admin

   1. admin will see the 5 pre filled courses that are concurrent with the jedi academny
   2. admin will be able to add, update, and delete courses
   3. admin will be able to see all the padawans that are in the jedi academny
   4. admin will be able to log out

   ## If user is padawan

   1. user will be brought to the landing page
   2. user will be able to see the courses that they are in
   3. user will be able to click on a course and see the other padawans that are in the course with them
      - user will not be able to see all the other padawans that are in the school with them UNLESS they are in the same course
   4. user (padawan) will be able to log out

## ROUTES

1. Padawans (Users)

   - register route -> ('/padawans/register') --> POST
   - login route -> ('/padawans/login') --> GET
   - log out route -> ('/padawans/logout') --> GET

2. Course

   - create courses route -> ('/courses/new') --> POST (must be admin)
   - update/edit courses route -> ('/courses/<id>') --> PUT (must be admin)
   - delete courses route -> ('/courses/<id>') --> Delete (must be admin)
   - list all padawans in a course -> ('/courses/<id>/padawans') --> GET (must be admin)
   - get all my courses (use current_user) -> ('/courses/current_user') --> GET
   - lists all courses --> GET /courses (admin and padawan can see)
   - lists all students in school --> GET /padawans -> (must be admin)

3. Enrollments
   - enroll -> ('/enrollments/<course_id>') --> POST

## MODELS

```
class Padawan(UserMixin, Model):
    full_name = CharField(unique = True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE
```

```
class Course(Model):
    title = CharField()
    description = CharField()
    start_date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE
```

```
class Enrollments(Model):
    course_id = ForeignKeyField(Enrollments, backref='courses')
    padawan_id = ForeignKeyField(Enrollments, backref='padawans')

    class Meta:
        database = DATABASE
```

```
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Course], safe=True)
    print("Created tables if they weren't already there")
    DATABASE.close()
```

# Wireframes

https://wireframe.cc/ATI4gT

# Stretch goals

- user (padawan) will be able to create their own lightsaber and battle others whom have the same one
