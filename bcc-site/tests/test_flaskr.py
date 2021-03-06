# -*- coding: utf-8 -*-
"""
    Flaskr Tests
    ~~~~~~~~~~~~

    Tests the Flaskr application.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
import tempfile
import pytest
import bcc


@pytest.fixture
def client():
    return bcc.app.test_client()



def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

@pytest.mark.skip(reason="no way of currently testing this")
def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, bcc.app.config['USERNAME'],
               bcc.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, bcc.app.config['USERNAME'] + 'x',
               bcc.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, bcc.app.config['USERNAME'],
               bcc.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


@pytest.mark.skip(reason="no way of currently testing this")
def test_messages(client):
    """Test that messages work"""
    login(client, bcc.app.config['USERNAME'],
          bcc.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
