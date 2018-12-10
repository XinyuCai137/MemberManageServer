#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Interviewers(Model):
    __table__ = 'interviewers'

    stu_id = StringField(primary_key=True, ddl='varchar(10)')
    email = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(10)')
    sex = StringField(ddl='varchar(10)')
    school = StringField(ddl='varchar(30)')
    phone = StringField(ddl='varchar(20)')
    passed = BooleanField()
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Interviews(Model):
    __table__ = 'interviews'
    
    stu_id = StringField(primary_key=True, ddl='varchar(10)')
    created_at = FloatField(default=time.time)
    grade_1 = IntegerField()
    grade_2 = IntegerField()
    grade_3 = IntegerField()
    grade_4 = IntegerField()
    grade_5 = IntegerField()
    extra = StringField(ddl='varchar(500)')


class Members(Model):
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
    phone = StringField(ddl='varchar(20)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Schools(Model):
    __table__ = 'schools'

    school = StringField(primary_key=True, ddl='varchar(30)')
    campus = StringField(ddl='varchar(10)')

class Voice_parts(Model):
    __table__ = 'voice_parts'

    voice_part = StringField(primary_key=True, ddl='varchar(2)')
    vp_lead1 = StringField(ddl='varchar(10)')
    vp_lead2 = StringField(ddl='varchar(10)')

class Departments(Model):
    __table__ = 'departments'

    department = StringField(primary_key=True, ddl='varchar(10)')
    dep_lead = StringField(ddl='varchar(10)')




