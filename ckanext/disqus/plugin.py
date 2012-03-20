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
        from pylons import request, tmpl_context as c 
        routes = request.environ.get('pylons.routes_dict')
        
        if routes.get('controller') == 'package' and \
            routes.get('action') == 'comments' and c.pkg.id:
            url = url_for(controller='package', action='read', 
                          id=c.pkg.name, qualified=True)
            data = {'name': self.disqus_name, 
                    'url': url,
                    'identifier': 'pkg-' + c.pkg.id}
            stream = stream | Transformer('body')\
                .append(HTML(html.BOTTOM_CODE % data))
            stream = stream | Transformer('body//div[@id="comments"]')\
                .append(HTML(html.COMMENT_CODE % data))
        
        return stream
    
