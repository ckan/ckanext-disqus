import logging

from genshi.core import TEXT
from genshi.input import HTML
from genshi.filters import Transformer

from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.interfaces import IConfigurable, IGenshiStreamFilter

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
            self.disqus_name = 'ckan'
        
    def filter(self, stream):
        """
        Required to implement IGenshiStreamFilter; will apply some HTML 
        transformations to the page currently rendered. Depends on Pylons
        global objects, how can this be fixed without obscuring the 
        inteface? 
        """
        
        from pylons import request, tmpl_context as c 
        from ckan.lib.helpers import url_for
        routes = request.environ.get('pylons.routes_dict')
        
        if routes.get('controller') == 'package' and \
            routes.get('action') == 'read' and c.pkg.id:
            data = {'name': self.disqus_name, 
                    'url': url_for(controller='package', action='read', 
                                   id=pkg.id),
                    'identifier': 'pkg-' + c.pkg.id}
            stream = stream | Transformer('body')\
                .append(HTML(html.BOTTOM_CODE % data))
            stream = stream | Transformer('body//div[@id="comments"]')\
                .append(HTML(html.COMMENT_CODE % data))
        
        if routes.get('controller') == 'home' and \
            routes.get('action') == 'index':
            data = {'name': self.disqus_name}
            stream = stream | Transformer('body//\
                div[@id="main"]//ul[@class="xoxo"]')\
                .append(HTML(html.LATEST_CODE % data))
        
        return stream
    
