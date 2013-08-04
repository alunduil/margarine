# Language: en

Feature: Article Create
  API SPECIFICATION:
    → POST /v1/articles/ -F "url=article.example.com"
    ← 202 Accepted
    ← Location: API URL for retrieval of Article
  QUERIES REQUIRED:
    * None

  Scenario: Add an article to margarine.
    Given a header, Content-Type, with a value of multipart/form-data
    And an URL, http://developer.rackspace.com/blog/got-python-questions.html
    When I POST /v1/articles/ to blend
    Then I receive a 202 status code
    And a message with the following JSON keys has been published:
      | key | value                                                         |
      | url | http://developer.rackspace.com/blog/got-python-questions.html |
      | _id | 0fb5c88e87535bc3a2514343b63682b0                              |

