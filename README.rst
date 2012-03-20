Disqus Extension
================

The Disqus extension allows site visitors to comment on individual 
packages using an AJAX-based commenting system. The downsides of 
this plugin are that comments are not stored locally and user 
information is not shared between CKAN and the commenting system.

Activating and Installing
-------------------------

In order to set up the Disqus plugin, you first need to go to 
disqus.com and set up a forum with your domain name. You will be 
able to choose a forurm name. 

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ git install -e hg+https://github.com/okfn/ckanext-disqus#egg=ckanext-disqus
 
This will also register a plugin entry point, so you now should be 
able to add the following to your CKAN .ini file:: 

 ckan.plugins = disqus <other-plugins>
 disqus.name = YOUR_DISQUS_NAME 

**At this point nothing will have happened**! To add comments into your pages
see the next section.
 
Using the Extension
-------------------

Comments Threads
~~~~~~~~~~~~~~~~

To have comment threads appear on pages, insert where you want the comments to
appear::

    <span class="insert-comment-thread"></span>

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

    <span class="insert-comment-recent"></span>

The recent comments widget will show 5 recent comments by default. This is not
currently customizable -- if you want to change it we suggest just insert the
disqus comments yourself as it is so simple to do.

Other widgets
~~~~~~~~~~~~~

Disqus offers many other widgets. Rather than providing these automatically as
part of this extension we suggest that theme developers incorporate the code
directly (note that you access the relevant config variables from the config
object passed into all templates).

