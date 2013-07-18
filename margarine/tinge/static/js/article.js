/**
 * Update the DOM with API information about the current article.
 */
function updateArticle(apiEndpoint) {
  $.get(apiEndpoint + "articles/" + getUrlVars()["id"],
      function(data) {
        document.title = data.title;

        $('@article-title').append(data.title);
        $('@article-author').append(data.author);
        $('@article-date').append(data.date);

        $('@article-tags').append(data.tags.join());

        $('@article-text').append(data.text);
      }, "json" )
}

/**
 * @brief Convert current page's URL query parameters to an associative array.
 *
 * @returns Associate array mapping query parameter names to values.
 *
 * Shamelessly implemented from:
 * http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html 
 *
 */
function getUrlVars() {
  var vars = [], hash;
  var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

  for ( var i = 0; i < hashes.length; i++) {
    hash = hashes[i].split('=');
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
  }

  return vars;
}

