/**
 * Inject Article information into active DOM.
 *
 * This function expects to be called from an article page and updates the
 * contents of the following items:
 *
 * :``.article-title``:  The title of the article.
 * :``.article-author``: The author of the article.
 * :``.article-date``:   The publication date of the article.
 * :``.article-text``:   The text contents of the article.
 *
 * Arguments
 * ---------
 *
 * :``apiEndpoint``: The endpoint that we can retrive article information from.
 *
 * .. note::
 *   The article information is expected to be JSON and have keys corresponding
 *   to the above information fields.
 */
function updateArticle(apiEndpoint) {
  $.get(apiEndpoint + "articles/" + getUrlVars()["id"],
      function(data) {
        document.title = "Margarine—" + data.title; 
        $('.article-title').append(data.title);

        $('.article-author').append(data.author);
        $('.article-date').append(data.date);

        $('.article-text').append(data.body);

        $('.article-tags').append(data.tags ? data.tags.join() : "");
      }, "json" )
}

/**
 * Convert current page's URL query parameters to an associative array.
 *
 * Returns
 * -------
 *
 * Associate array mapping query parameter names to values.
 *
 * ..note::
 *   Shamelessly implemented from:
 *   http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html 
 */
function getUrlVars() {
  var vars = [], hash;
  var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

  for ( var i = 0; i < hashes.length; i++ ) {
    hash = hashes[i].split('=');
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
  }

  return vars;
}
