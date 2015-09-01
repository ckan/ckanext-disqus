Disqus Extension
================

The Disqus extension allows site visitors to comment on individual
packages using an AJAX-based commenting system. The downsides of
this plugin are that comments are not stored locally and user
information is not shared between CKAN and the commenting system.

**Note: This extension requires ckan 1.7 or higher**

Activating and Installing
-------------------------

In order to set up the Disqus plugin, you first need to go to
disqus.com and set up a forum with your domain name. You will be
able to choose a forurm name.

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ pip install -e git+https://github.com/okfn/ckanext-disqus#egg=ckanext-disqus

For ckan versions before 2.0, please use the `release-v1.8` branch.

This will also register a plugin entry point, so you now should be
able to add the following to your CKAN .ini file::

 ckan.plugins = disqus <other-plugins>
 disqus.name = YOUR_DISQUS_NAME

At this point, each dataset view page will have Disqus comments. To add comments into
other pages, see the next section.

Disqus will use window.location.href as the `disqus_url`. It is sometimes
helpful, especially during development, to specify the base url for disqus to
use instead. This can be added to the CKAN .ini file::

 disqus.disqus_url = my_staging.server.com

Do not include 'http://' or a trailing slash.


Using the Extension
-------------------

Comments Threads
~~~~~~~~~~~~~~~~

To have comment threads appear on pages, insert into templates where you want the comments to
appear::

    {{h.disqus_comments()}}

Note for theme developers: the extensions tries to generate a disqus_identifier
of the form::

    {controller/domain-object-name}::{id}

Where controller = 'group' in the group section, 'dataset' in the dataset
section (note that this differs from controller name internally which is still
package), 'resource'  for resources etc. This identifier will be useful if you
want to then reference this comment (e.g. for comment counts) elsewhere in the
site.

Recent comments
~~~~~~~~~~~~~~~

Insert on pages where you want recent comments to appear::

    {{h.disqus_recent()}}

The recent comments widget will show 5 recent comments by default.  To show 10 recent comments use the following::

    {{h.disqus_recent(num_comments=10)}}

Other widgets
~~~~~~~~~~~~~

Disqus offers many other widgets. Rather than providing these automatically as
part of this extension we suggest that theme developers incorporate the code
directly (note that you access the relevant config variables from the config
object passed into all templates).

Single Sign On
~~~~~~~~~~~~~

Disqus offers a "Single Sign On" option which allows users to submit comments using
the local username/password rather than require a seperate disqus account.
For instructions on how to set things up on the Disqus end (i.e. create API keys)
see:
https://help.disqus.com/customer/portal/articles/236206-integrating-single-sign-on

To integrate with this CKAN plugin, you must store your Public and Secret keys
in the CKAN ini file::

    ckan.plugins = disqus <other-plugins>
    disqus.name = YOUR_DISQUS_NAME
    disqus.secret_key  = YOUR_DISQUS_SECRET_KEY
    disqus.public_key  = YOUR_DISQUS_PUBLIC_KEY
