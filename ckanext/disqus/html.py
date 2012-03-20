COMMENT_CODE = """
 <h4>Comments</h4> 
<div id="disqus_thread"></div>
<script type="text/javascript">
  var disqus_identifier = "%(identifier)s";
  var disqus_url = "%(url)s";
  var disqus_developer = true;
  (function() {
   var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
   dsq.src = 'http://%(name)s.disqus.com/embed.js';
   (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
  })();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript=%(name)s">comments powered by Disqus.</a></noscript>
"""

BOTTOM_CODE = """
<script type="text/javascript">
var disqus_shortname = '%(name)s';
(function () {
  var s = document.createElement('script'); s.async = true;
  s.src = 'http://disqus.com/forums/%(name)s/count.js';
  (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
}());
</script>
"""

LATEST_CODE = """
<li id="recentcomments" class="widget-container widget_text">
    <h2 class="dsq-widget-title">Recent Comments</h2>
    <div>
    <script type="text/javascript" src="http://disqus.com/forums/%(name)s/recent_comments_widget.js?num_items=5&hide_avatars=0&avatar_size=32&excerpt_length=200"></script>
    </div>
</li>"""