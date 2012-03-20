COMMENT_CODE = """
<div class="ckan-comment-thread">
  <h3>Comments</h3> 
  <div id="disqus_thread"></div>
</div>
<script type="text/javascript">
  var disqus_shortname = "%(name)s";
  var disqus_identifier = disqus_identifier || "%(identifier)s";
  var disqus_developer = %(disqus_developer)s;

  (function() {
      var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
      dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
      (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
  })();
</script>
<noscript>Please enable JavaScript to view the comments.</noscript>
"""

RECENT_COMMENTS = """
<div class="ckan-recent-comments">
var disqus_shortname = "%(name)s";
<div id="recentcomments" class="dsq-widget"><h2 class="dsq-widget-title">Recent
Comments</h2><script type="text/javascript"
src="http://ckan.disqus.com/recent_comments_widget.js?num_items=5&hide_avatars=0&avatar_size=32&excerpt_length=200"></script></div>
</div>
"""
