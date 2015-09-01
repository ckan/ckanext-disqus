import logging
import base64
import hashlib
import hmac
import simplejson
import time

from ckan.common import request
from ckan.lib.helpers import url_for_static_or_external
import ckan.plugins as p

disqus_translations = {
    'de': 'de',
    'es': 'es_ES',
    'sv': 'sv_SE',
    'pt': 'pt_EU',
    'sr': 'sr_CYRL',
    'sr_Latn': 'sr_LATIN',
    'no': 'en',  # broken no translation available
}

# These are funny disqus language codes
# all other codes are two letter language code

# Portuguese (Brazil) = pt_BR
# Portuguese (European) = pt_EU
# Serbian (Cyrillic) = sr_CYRL
# Serbian (Latin) = sr_LATIN
# Spanish (Argentina) = es_AR
# Spanish (Mexico) = es_MX
# Spanish (Spain) = es_ES
# Swedish = sv_SE

log = logging.getLogger(__name__)


class Disqus(p.SingletonPlugin):
    '''
    Insert javascript fragments into package pages and the home page to allow
    users to view and create comments on any package.
    '''
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def configure(self, config):
        '''
        Called upon CKAN setup, will pass current configuration dict to the
        plugin to read custom options.  To implement Disqus Single Sign On,
        you must have your secret and public key in the ckan config file. For
        more info on Disqus SSO see:
        https://help.disqus.com/customer/portal/articles/236206-integrating-single-sign-on
        '''
        disqus_name = config.get('disqus.name', None)
        disqus_secret_key = config.get('disqus.secret_key', None)
        disqus_public_key = config.get('disqus.public_key', None)
        disqus_url = config.get('disqus.disqus_url', None)
        site_url = config.get('ckan.site_url', None)
        site_title = config.get('ckan.site_title', None)
        if disqus_name is None:
            log.warn("No disqus forum name is set. Please set \
                'disqus.name' in your .ini!")
        config['pylons.app_globals'].has_commenting = True

        disqus_developer = p.toolkit.asbool(config.get('disqus.developer',
                                                       'false'))
        disqus_developer = str(disqus_developer).lower()
        # store these so available to class methods
        self.__class__.disqus_developer = disqus_developer
        self.__class__.disqus_name = disqus_name
        self.__class__.disqus_secret_key = disqus_secret_key
        self.__class__.disqus_public_key = disqus_public_key
        self.__class__.disqus_url = disqus_url
        self.__class__.site_url = site_url
        self.__class__.site_title = site_title

    def update_config(self, config):
        # add template directory to template path
        p.toolkit.add_template_directory(config, 'templates')

    @classmethod
    def language(cls):
        lang = p.toolkit.request.environ.get('CKAN_LANG')
        if lang in disqus_translations:
            lang = disqus_translations[lang]
        else:
            lang = lang[:2]
        return lang

    @classmethod
    def disqus_comments(cls):
        '''Add Disqus Comments to the page.'''

        c = p.toolkit.c

        # Get user info to send for Disqus SSO

        # Set up blank values
        message = 'blank'
        sig = 'blank'
        timestamp = 'blank'

        # Get the user if they are logged in.
        user_dict = {}
        try:
            user_dict = p.toolkit.get_action('user_show')({'keep_email': True},
                                                          {'id': c.user})

        # Fill in blanks for the user if they are not logged in.
        except:
            user_dict['id'] = ''
            user_dict['name'] = ''
            user_dict['email'] = ''

        # Create the SSOm data.
        SSOdata = simplejson.dumps({
            'id': user_dict['id'],
            'username':  user_dict['name'],
            'email': user_dict['email'],
            })

        message = base64.b64encode(SSOdata)
        # generate a timestamp for signing the message
        timestamp = int(time.time())
        # generate our hmac signature
        sig = ''
        if cls.disqus_secret_key is not None:
            sig = hmac.HMAC(cls.disqus_secret_key, '%s %s' %
                            (message, timestamp), hashlib.sha1).hexdigest()

        # we need to create an identifier
        try:
            identifier = c.controller
            if identifier == 'package':
                identifier = 'dataset'
            if c.current_package_id:
                identifier += '::' + c.current_package_id
            elif c.id:
                identifier += '::' + c.id
            else:
                # cannot make an identifier
                identifier = ''
            # special case
            if c.action == 'resource_read':
                identifier = 'dataset-resource::' + c.resource_id
        except:
            identifier = ''
        data = {'identifier': identifier,
                'developer': cls.disqus_developer,
                'language': cls.language(),
                'disqus_shortname': cls.disqus_name,

                # start Koebrick change
                'site_url': cls.site_url,
                'site_title': cls.site_title,
                'message': message,
                'sig': sig,
                'timestamp': timestamp,
                'pub_key': cls.disqus_public_key}

        return p.toolkit.render_snippet('disqus_comments.html', data)

    @classmethod
    def disqus_recent(cls, num_comments=5):
        '''Add Disqus recent comments to the page. '''
        data = {'disqus_shortname': cls.disqus_name,
                'disqus_num_comments': num_comments}
        return p.toolkit.render_snippet('disqus_recent.html', data)

    @classmethod
    def current_disqus_url(cls, ):
        '''If `disqus.disqus_url` is defined, return a fully qualified url for
        the current page with `disqus.disqus_url` as the base url,'''

        if cls.disqus_url is None:
            return None

        return url_for_static_or_external(request.environ['CKAN_CURRENT_URL'],
                                          qualified=True, host=cls.disqus_url)

    def get_helpers(self):
        return {'disqus_comments': self.disqus_comments,
                'disqus_recent': self.disqus_recent,
                'current_disqus_url': self.current_disqus_url}
