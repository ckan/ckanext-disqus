import logging

from genshi.core import TEXT
from genshi.input import HTML
from genshi.filters import Transformer

from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.interfaces import IConfigurable, IGenshiStreamFilter
from ckan.lib.helpers import url_for

import html

log = logging.getLogger(__name__)

class Disqus(SingletonPlugin):
    """
    Insert javascript fragments into package pages and the home page to
    allow users to view and create comments on any package.
    """

    implements(IConfigurable)
    implements(IGenshiStreamFilter)

    def configure(self, config):
        """
        Called upon CKAN setup, will pass current configuration dict
        to the plugin to read custom options.
        """
        self.disqus_name = config.get('disqus.name', None)
        self.disqus_developer = config.get('disqus.developer', 'false')
        if self.disqus_name is None:
            log.warn("No disqus forum name is set. Please set \
                'disqus.name' in your .ini!")
        config['pylons.app_globals'].has_commenting = True

    def filter(self, stream):
        """
        Required to implement IGenshiStreamFilter; will apply some HTML
        transformations to the page currently rendered. Depends on Pylons
        global objects, how can this be fixed without obscuring the
        inteface?
        """
        from pylons import request
        routes = request.environ.get('pylons.routes_dict')
        try:
            identifier = routes.get('controller')
            if identifier == 'package':
                identifier = 'dataset'
            if routes.get('id'):
                identifier += '::' + routes.get('id')
            else:
                # cannot make an identifier
                identifier = ''
            # special case
            if routes.get('action') == 'resource_read':
                identifier = 'dataset-resource::' + routes.get('resource_id')
        except:
            identifier = ''

        data = {'name': self.disqus_name,
                'identifier': identifier,
                'disqus_developer': self.disqus_developer
            }
        comment_code = HTML(html.COMMENT_CODE % data)
        stream = stream | Transformer('//span[@class="insert-comment-thread"]')\
                 .after(comment_code)

        recent = HTML(html.RECENT_COMMENTS % data)
        stream = stream | Transformer('//span[@class="insert-comment-recent"]')\
                 .after(recent)

        return stream

