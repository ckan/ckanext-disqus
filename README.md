
Disqus Plugin 
=============

The Disqus plugin allows site visitors to comment on individual 
packages using an AJAX-based commenting system. The downsides of 
this plugin are that comments are not stored locally and user 
information is not shared between CKAN and the commenting system.

Activating and Installing
-------------------------

In order to set up the Disqus plugin, you first need to go to 
disqus.com and set up a forum with your domain name. You will be 
able to choose a forurm name. 

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ pip install -e hg+gttps://okfn@bitbucket.org/okfn/ckanext-disqus#egg=ckanext-disqus
 
This will also register a plugin entry point, so you now should be 
able to add the following to your CKAN .ini file:: 

 ckan.plugins = disqus <other-plugins>
 disqus.name = YOUR_DISQUS_NAME 
 
After clearing your cache and reloading the web server, comments 
should now be available on package pages and on the home page. 

