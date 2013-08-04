# Language: en

Feature: Article Read
  API SPECIFICATION:
    → GET /v1/articles/UUID5 (with hyphens)
    ← 200 Found (404 if no body found)
    ← Content-Type: application/json
    ← Access-Control-Allow-Origin: Frontend URL # TODO Add Test for configuration?
    ← JSON article object

  QUERIES REQUIRED:
    * Can I have the properties of the article with _id of the UUID5?
    * Can I have the body of the article with _id of the UUID5?

  Scenario: Read an existing article from margarine. (Default Content-Type)
    Given an article with the following properties is available:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | created_at | 1375629048391                                                 |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |
    When I GET /v1/articles/ to blend
    Then I receive a 404 status code
    
  Scenario: Read an existing article from margarine. (Default Content-Type)
    Given an article with the following properties is available:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |
    When I GET /v1/articles/ to blend
    Then I receive a 200 status code
    And I receive a header, Access-Control-Allow-Origin, with a value of FRONTEND_URL
    And I receive a body with the following JSON keys:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |

  Scenario: Read an existing article from margarine. (Content-Type: application/json)
    Given an article with the following properties is available:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |
    When I GET /v1/articles/ to blend
    Then I receive a 200 status code
    And I receive a header, Access-Control-Allow-Origin, with a value of FRONTEND_URL
    And I receive a header, Content-Type, with the value application/json
    And I receive a body with the following JSON keys:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |

