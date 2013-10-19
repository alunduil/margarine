/**
 * Set the blend_url so that it's globally accessible.
 *
 * This function sets a window property, ``margarine_blend_url``, that contains
 * the URL that an AJAX calls should hit.  This allows other functions to have
 * this information without needing a parameter.
 *
 * Arguments
 * ---------
 *
 * :``blend_url``: The endpoint that we can hit blend at.
 */
function setBlendUrl(blend_url) {
  window.margarine_blend_url = blend_url;
}
