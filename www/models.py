#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)




class Interviewer(Model):
    __table__ = 'interviewers'

    stu_id = StringField(primary_key=True, ddl='varchar(10)')
    email = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(10)')
    sex = StringField(ddl='varchar(10)')
    admin = BooleanField()
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Interview(Model):
    __table__ = 'interviews'

    stu_id = StringField(primary_key=True, ddl='varchar(10)')



class Member(Model):
    __table__ = 'members'

    stu_id = StringField(primary_key=True, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    sex = StringField(ddl='varchar(10)')
    school = StringField(ddl='varchar(30)')
    voice_part = StringField(ddl='varchar(2)')
    department = StringField(ddl='varchar(10)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Voice(Model):
    __table__ = 'voice_parts'

    voice_part = StringField(primary_key=True, ddl='varchar(2)')
    vp_lead1 = StringField(ddl='varchar(10)')
    vp_lead2 = StringField(ddl='varchar(10)')



class School(Model):
    __table__ = 'schools'

    school = StringField(primary_key=True, ddl='varchar(30)')
    campus = StringField(ddl='varchar(10)')


class Department(Model):
    __table__ = 'departments'

    department = StringField(primary_key=True, ddl='varchar(10)')
    dep_lead = StringField(ddl='varchar(10)')

# class Blog(Model):
#     __table__ = 'blogs'

#     id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
#     user_id = StringField(ddl='varchar(50)')
#     user_name = StringField(ddl='varchar(50)')
#     user_image = StringField(ddl='varchar(500)')
#     name = StringField(ddl='varchar(50)')
#     summary = StringField(ddl='varchar(200)')
#     content = TextField()
#     created_at = FloatField(default=time.time)

# class Comment(Model):
#     __table__ = 'comments'

#     id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
#     blog_id = StringField(ddl='varchar(50)')
#     user_id = StringField(ddl='varchar(50)')
#     user_name = StringField(ddl='varchar(50)')
#     user_image = StringField(ddl='varchar(500)')
#     content = TextField()
#     created_at = FloatField(default=time.time)
