import logging
import os

from webhelpers.html.tags import literal
from paste.deploy.converters import asbool
from pylons import c, request

import ckan.lib.base as base
import ckan.plugins as plugins

import ckanext.disqus


disqus_translations = {
    'de' : 'de_inf',
    'es' : 'es_ES',
    'sv' : 'sv_SE',
    'pt' : 'pt_EU',
    'sr' : 'sr_CYRL',
    'sr_Latn' : 'sr_LATIN',
    'no' : 'en', # broken no translation available
}

# These are funny disqus language codes
# all other codes are two letter language code
##German (Formal) = de_formal
##German (Informal) = de_inf
##Portuguese (Brazil) = pt_BR
##Portuguese (European) = pt_EU
##Serbian (Cyrillic) = sr_CYRL
##Serbian (Latin) = sr_LATIN
##Spanish (Argentina) = es_AR
##Spanish (Mexico) = es_MX
##Spanish (Spain) = es_ES
##Swedish = sv_SE

log = logging.getLogger(__name__)

def configure_template_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_template_paths')

def configure_public_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_public_paths')

def configure_served_directory(config, relative_path, config_var):
    'Configure serving of public/template directories.'
    assert config_var in ('extra_template_paths', 'extra_public_paths')
    this_dir = os.path.dirname(ckanext.disqus.__file__)
    absolute_path = os.path.join(this_dir, relative_path)
    if absolute_path not in config.get(config_var, ''):
        if config.get(config_var):
            config[config_var] += ',' + absolute_path
        else:
            config[config_var] = absolute_path

class Disqus(plugins.SingletonPlugin):
    """
    Insert javascript fragments into package pages and the home page to
    allow users to view and create comments on any package.
    """
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def configure(self, config):
        """
        Called upon CKAN setup, will pass current configuration dict
        to the plugin to read custom options.
        """
        disqus_name = config.get('disqus.name', None)
        if disqus_name is None:
            log.warn("No disqus forum name is set. Please set \
                'disqus.name' in your .ini!")
        config['pylons.app_globals'].has_commenting = True

        disqus_developer = asbool(config.get('disqus.developer', 'false'))
        disqus_developer = str(disqus_developer).lower()
        # store these so available to class methods
        self.__class__.disqus_developer = disqus_developer
        self.__class__.disqus_name = disqus_name

    def update_config(self, config):
        # add template directory to template path
        configure_template_directory(config, 'templates')


    @classmethod
    def language(cls):
        lang = request.environ.get('CKAN_LANG')
        if lang in disqus_translations:
            lang = disqus_translations[lang]
        else:
            lang = lang[:2]
        return lang


    @classmethod
    def disqus_comments(cls):
        '''  '''
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
        data = {'identifier' : identifier,
                'developer' : cls.disqus_developer,
                'language' : cls.language(),
                'disqus_shortname': cls.disqus_name,}
        return literal(base.render('disqus-comments.html', data))

    @classmethod
    def disqus_recent(cls):
        '''  '''
        data = {'disqus_shortname': cls.disqus_name,}
        return literal(base.render('disqus-recent.html', data))

    def get_helpers(self):
        return {'disqus_comments' : self.disqus_comments,
                'disqus_recent' : self.disqus_recent,}
