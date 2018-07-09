# -*- coding: utf-8 -*-

import logging

import ckan.lib.base as base
import ckan.model as model
import ckan.lib.render
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.lib.mailer as mailer
import ckan.lib.i18n as i18n

import pylons.config as config

render = base.render

from ckan.common import json, request, c, g, response, _

log = logging.getLogger(__name__)

class DisqusController(base.BaseController):

    def notify(self):
        prev_lang = i18n.get_lang()
        i18n.set_lang(config.get('ckan.locale_default', 'en'))

        comment_id = request.params.get('comment_id')
        comment = request.params.get('comment')
        pkg_id = request.params.get('pkg_id')
        recipient_name_field = config.get('disqus.notify.name_field')
        recipient_email_field = config.get('disqus.notify.email_field')

        mail_sent = False

        if pkg_id is not None:
            pkg = logic.get_action('package_show')({'ignore_auth': True}, {'id': pkg_id})
            if recipient_email_field in pkg and pkg.get(recipient_email_field, '') != '':
                url_path = toolkit.url_for(controller='package', action='read', id=pkg_id)
                url = '%s%s' % (request.host_url, url_path)
                msg_fields = {
                        'url': url,
                        'title': pkg["title"],
                        'comment': comment
                        }
                title = _(u'New comment for dataset "%(title)s"') % msg_fields
                msg = _(u'<p>The dataset <a href="%(url)s">"%(title)s"</a> has received a new comment:</p><p>%(comment)s</p>') % msg_fields
                recipient_name = pkg.get(recipient_name_field, _(u'Dataset maintainer'))
                recipient_email = pkg.get(recipient_email_field)
                try:
                    mailer.mail_recipient(recipient_name, recipient_email, title, msg)
                    mail_sent = True
                except mailer.MailerException, e:
                    log.error('Could not send disqus notification mail: %s' % e)


        data = {'comment_id' : comment_id,
                'pkg_id': pkg_id,
                'mail_sent': mail_sent}
        result = render('disqus_callback.html', data)
        i18n.set_lang(prev_lang)
        return result
