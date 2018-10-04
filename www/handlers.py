
import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from model import Member, next_id

@get('/')
async def index(request):
    members = await Menmber.findAll()
    return {
        '__template__': 'test.html',
        'members': members
    }