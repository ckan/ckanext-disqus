# -*- coding: utf-8 -*- 
import logging

import ckan.lib.base as base
import ckan.model as model
import ckan.lib.render
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.lib.mailer as mailer

import pylons.config as config

render = base.render

from ckan.common import json, request, c, g, response

log = logging.getLogger(__name__)

class DisqusController(base.BaseController):

    def callback(self):
        user = model.User.get('admin')
        context = { 'model':model,'user': 'admin','session':model.Session, 'for_view': True }
        cid = request.params.get('comment_id')
        comment = request.params.get('comment')
        id = request.params.get('pkg_id')

        if id != "":
            data_dict = {}
            data_dict["id"] = id
            pkg = logic.get_action('package_show')(context, data_dict)
            callback_field = config.get('disqus.callback.field', "None")
            mail_sent = 0
            if callback_field in pkg and pkg.get(callback_field) <> None:
                url = request.host_url + toolkit.url_for(controller='package', action='read', id=id)
                msg = u'Zum Datensatz mit der ID %s - "%s"\r\n wurde ein neuer Kommentar mit folgendem Inhalt abgegeben:\r\n\r\n"%s"\r\n\r\nLink zum Datensatz: %s\r\n\r\nHinweis: Sie erhalten diese Email, weil Ihre Email-Adresse beim Datensatz "%s" als Kontaktmöglichkeit angegeben wurde. Wenn Sie dies ändern möchten, kontaktieren Sie bitte Ihre Open-Data-Koordinierungsstelle. ' % (id, pkg["title"], comment, url, pkg["title"])
                mailer.mail_recipient('Datenverantwortliche/r', pkg.get(callback_field, ""),  'Neuer Kommentar zum Datensatz', msg)
                mail_sent = 1

        data = {'comment_id' : cid,
                'pkg_id': id,
                'mail_sent': mail_sent}                
        return render('disqus_callback.html', data)