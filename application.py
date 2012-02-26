import os

from framework import *
from db import root, db
import transaction

from models import *

try:
    os.remove('/tmp/Data.fs.lock')
    print 'had to remove lock'
except OSError:
    pass

root.setdefault('users', {})
root.setdefault('blogs', [])
transaction.commit()

application = App()
application.template_path = os.path.dirname(__file__) + '/templates'

@application.route('/user/create/(.+)/')
def create_user(request, username):
    root['users'][username] = User(username)
    root._p_changed=True
    transaction.commit()

    return HttpResponse('created user %s' % username)

@application.route('/user/')
def list_users(request):
    users = root['users'].values()
    return application.render(request, 'users.html', {'users': users})

@application.route('/blog/create/(.+)/(.+)/')
def create_blog(request, username, text):
    blog = Blog(user=root['users'][username], text=text)
    root['blogs'].append(blog)
    root._p_changed = True
    transaction.commit()
    return HttpResponse('successssss')


@application.route('/blog/')
def list_blogs(request):
    blogs = root['blogs']
    return application.render(request, 'blogs.html', {'blogs': blogs})
