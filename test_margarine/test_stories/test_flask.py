from lettuce import *

from margarine.blend import BLEND

from test_margarine.test_stories.test_helpers import URL_REGEXP

@step("I (POST|PUT|GET|DELETE) " + URL_REGEXP + "to blend")
def blend_http_request(step, method, url):
    BLEND.config["TESTING"] = True
    world.application = BLEND.test_client()

    world.response = getattr(world.application, method.lower())(url), data = world.data)
