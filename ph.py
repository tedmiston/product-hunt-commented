"""Print every comment you've made on Product Hunt."""

import os
import shelve
import sys

import requests


def extend(dict1, dict2):
    """Create a new dict from the values of dict1 added/updated by the values from dict2."""
    return dict(dict1, **dict2)


class ProductHunt(object):
    """A thin wrapper around the Product Hunt API."""
    BASE_URL = 'https://api.producthunt.com/v1'

    def __init__(self):
        try:
            self.DEV_TOKEN = os.environ['PRODUCT_HUNT_DEV_TOKEN']
        except:
            sys.exit('Don\'t forget to store your dev token in the environment variable PRODUCT_HUNT_DEV_TOKEN.')
        self.headers = {'authorization': 'Bearer {}'.format(self.DEV_TOKEN)}
        self.shelve = shelve.open('my_comments')
        self.etag_comments = self.shelve.get('etag_comments')
        self.etag_user = self.shelve.get('etag_user')
        self.my_comments = self.shelve.get('comments')
        self.user = self.shelve.get('user')

    def __del__(self):
        self.shelve['etag_comments'] = self.etag_comments
        self.shelve['etag_user'] = self.etag_user
        self.shelve['comments'] = self.my_comments
        self.shelve['user'] = self.user
        self.shelve.close()

    def _build_url(self, path):
        return '{}/{}'.format(self.BASE_URL, path)

    def _exit_with_error(self, request):
        if request.status_code == requests.codes.unauthorized:
            short_message = 'Product Hunt auth token is invalid.'
        else:
            short_message = 'Unknown error'
        long_message = request.json()['error_description']
        error_message = 'Error: {}\n\n{}'.format(short_message, long_message)
        sys.exit(error_message)

    def fetch_me(self):
        """Retrieve my user account details."""
        url = self._build_url('me')
        headers = {'If-None-Match': self.etag_user}
        r = requests.get(url, headers=extend(self.headers, headers))
        if r.status_code == requests.codes.unauthorized:
            self._exit_with_error(r)
        elif r.status_code == requests.codes.ok:
            u = r.json()['user']
            self.etag_user = r.headers['etag']
            self.user = User(u['id'], u['username'], u['name'])

    def fetch_user_comments(self, user_id):
        """Retrieve all comments for a user."""        
        url = self._build_url('users/{}/comments'.format(user_id))
        headers = {'If-None-Match': self.etag_comments}
        r = requests.get(url, headers=extend(self.headers, headers))
        if r.status_code == requests.codes.unauthorized:
            self._exit_with_error(r)
        elif r.status_code == requests.codes.ok:
            self.etag_comments = r.headers['etag']
            self.my_comments = [Comment(i['body'], i['post']['name']) for i in r.json()['comments']]

    def fetch_my_comments(self):
        """Retrieve all of my comments."""
        self.fetch_me()
        self.fetch_user_comments(self.user.user_id)

    def print_my_comments(self):
        print 'Comments for {full_name} #{user_id} (@{username})\n'.format(
            full_name=self.user.full_name, user_id=self.user.user_id, username=self.user.username)

        for idx, comment in enumerate(self.my_comments):
            print u'{idx}.) on "{post_title}":\n> "{comment_body}"\n'.format(
                comment_body=comment.body, idx=idx+1, post_title=comment.post_title)


class User(object):
    """A Product Hunt user."""

    def __init__(self, user_id, username, full_name):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name


class Comment(object):
    """A Product Hunt comment."""

    def __init__(self, body, post_title):
        self.body = body
        self.post_title = post_title


def main():
    ph = ProductHunt()
    ph.fetch_my_comments()
    ph.print_my_comments()


if __name__ == '__main__':
    main()
