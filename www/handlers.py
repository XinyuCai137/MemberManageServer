# -*- coding: utf-8 -*-
"""
Created on Wed Oct 3 2018
@author: Vegelofe
Learned from Michael Liao
"""

'''
async web application.
'''

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

# import markdown2

from aiohttp import web

from coroweb import get, post
from apis import APIValueError, APIResourceNotFoundError, APIError, APIPermissionError

from models import Interviews, Interviewers, Members, Schools, Voice_parts, Departments
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError('Administration error!')

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.stu_id, user.passwd, expires, _COOKIE_KEY)
    L = [user.stu_id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        stu_id, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from Members.find(stu_id)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (stu_id, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
def index(request):
    return {
        '__template__': 'index.html'
    }

@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }

@get('/signup')
def signup():
    return {
        '__template__': 'signup.html'
    }

@get('/wechat')
def wechat():
    return{
        '__template__': 'wechat.html'
    }

@get('/user/enquiry')
def enquiry():
    return{
        '__template__': 'enquiry.html'
    }

@get('/user/api/enquiry')
def get_enquiry():
    members = yield from Members.findAll()
    return members

@post('/user/api/optional_enquiry')
def optional_enquiry(*, option):
    if not option:
        raise APIValueError('option', 'No option')
    where = ''
    args = []
    if option['sex'] != 'all':
        args.append(option['sex'])
        where += 'sex=?'
    if option['school'] != 'all':
        args.append(option['school'])
        if where:
            where += 'and school=?'
        else:
            where += 'school=?'
    if option['voice_part'] != 'all':
        args.append(option['voice_part'])
        if where:
            where += 'and voice_part=?'
        else:
            where += 'voice_part=?'
    if option['department'] != 'all':
        args.append(option['department'])
        if where:
            where += 'and department=?'
        else:
            where += 'department=?'
    members = yield from Members.findAll(where, args)
    return members

@get('/user/personal')
def personal(request):
    user = yield from Members.find(request.__user__.stu_id)
    return{
        '__template__': 'member.html',
        'user': user
    }

@post('/manage/api/members')
def manage_members(*, members):
    for member in members:
        member_ = yield from Members.find(member['stu_id'])
        member_.voice_part = member['voice_part']
        member_.department = member['department']
        yield from member_.update() 
    return members      



@get('/user/api/personal')
def get_personal(request):
    user = yield from Members.find(request.__user__.stu_id)
    return user

@post('/user/api/edit_personal')
def edit_personal(*,member):
    user = yield from Members.find(member['stu_id'])
    user.name = member['name']
    user.stu_id = member['stu_id']
    user.sex = member['sex']
    user.email = member['email']
    user.phone = member['phone']
    user.school = member['school']
    user.voice_part = member['voice_part']
    user.department = member['department']
    yield from user.update()
    return user

@get('/manage/interview')
def interview():
    return {
        '__template__': 'interview.html'
    }

@get('/manage/interview/select')
def interview_select():
    return {
        '__template__': 'interview_select.html',
    }

@get('/manage/api/get_interviews')
def get_interviews():
    interviews = yield from Interviews.findAll()
    for interview in interviews:
        interviewer = yield from Interviewers.find(interview.stu_id)
        interview['sex'] = interviewer.sex
        interview['passed'] = interviewer.passed
    return interviews

@post('/manage/api/submit_interview_result')
def submit_interview_result(*, interviews):
    for interview in interviews:
        interviewer = yield from Interviewers.find(interview['stu_id'])
        interviewer.passed = True if interview['passed'] == 'true' else False
        yield from interviewer.update()
    interviews_ = yield from Interviews.findAll()
    for interview in interviews_:
        interviewer = yield from Interviewers.find(interview.stu_id)
        interview['sex'] = interviewer.sex
        interview['passed'] = interviewer.passed
    return interviews_

@post('/manage/api/interview_grade')
def interview_grade(*, stu_id, grade_1, grade_2, grade_3, grade_4, grade_5, extra):
    if not stu_id:
        raise APIValueError('stu_id', 'Invalid stu_id.')
    interviews = yield from Interviews.findAll('stu_id=?', [stu_id])
    if len(interviews) == 0:
        interviewers = yield from Interviewers.findAll('stu_id=?', [stu_id])
        if len(interviewers) == 0:
            raise APIValueError('stu_id', 'This stu_id does not exist.')
        interview = Interviews(stu_id=stu_id, grade_1=grade_1, grade_2=grade_2, grade_3=grade_3, grade_4=grade_4, grade_5=grade_5, extra=extra)
        yield from interview.save()
    else:
        interview = interviews[0]
        interview.grade_1 = grade_1
        interview.grade_2 = grade_2
        interview.grade_3 = grade_3
        interview.grade_4 = grade_4
        interview.grade_5 = grade_5
        interview.extra = extra
        yield from interview.update()
    
        r = json.dumps(interview, ensure_ascii=False).encode('utf-8')
        return r

@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from Members.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.stu_id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
def api_register_user(*, email, passwd):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    members = yield from Members.findAll('email=?', [email])
    if len(members) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    interviewers = yield from Interviewers.findAll('email=?', [email])
    if len(interviewers) == 0:
        raise APIValueError('register:failed', 'You have not sign up')
    if interviewers[0].passed == False:
        raise APIValueError('register:failed', 'You have not passed the interview')
    

    interviewers = yield from Interviewers.findAll('email=?', [email])
    interviewer = interviewers[0]
    stu_id = interviewer.stu_id
    sha1_passwd = '%s:%s' % (stu_id, passwd)
    member = Members(stu_id=stu_id, name=interviewer.name.strip(), email=email, sex=interviewer.sex, school=interviewer.school, phone=interviewer.phone, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), voice_part='N', department='N', image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from member.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(member, 86400), max_age=86400, httponly=True)
    member.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(member, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/signup')
def api_signup(*, email, name, stu_id, sex, school, phone):
    if not name or not name.strip():
        raise APIValueError('name')
    if not stu_id or not stu_id.strip():
        raise APIValueError('stu_id')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    interviewers = yield from Interviewers.findAll('stu_id=?', [stu_id])
    if len(interviewers) > 0:
        raise APIError('signup:failed', 'email', 'Email is already in use.')
 
    interviewer = Interviewers(stu_id=stu_id.strip(), name=name.strip(), email=email, sex=sex, school=school, phone=phone, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from interviewer.save()

    r = json.dumps(interviewer, ensure_ascii=False).encode('utf-8')
    return r
