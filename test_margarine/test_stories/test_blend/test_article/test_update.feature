# Language: en

Feature: Article Update
  API SPECIFICATION:
    → PUT /v1/articles/UUID5 (with hyphens)
    ← 405 Method Not Allowed

  QUERIES REQUIRED:
    * None

  Scenario: Update an existing article in margarine.
    Given an article with the following properties is available:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |
    When I PUT /v1/articles/
    Then I receive a 405 status code

  Scenario: Update a non-existant article in margarine.
    Given an article with the following properties is available:
      | property   | value                                                         |
      | _id        | 0fb5c88e87535bc3a2514343b63682b0                              |
      | body       | HTML (Stub for testing purposes)                              |
      | created_at | 1375629048391                                                 |
      | etag       | bf6285d832a356e1bf509a63edc8870f                              |
      | parsed_at  | 1375629049416                                                 |
      | size       | 31052                                                         |
      | url        | http://developer.rackspace.com/blog/got-python-questions.html |
    When I PUT /v1/articles/
    Then I receive a 405 status code

