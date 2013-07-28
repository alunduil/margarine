# language: en

Feature: Login

  # GET /v1/users/alunduil/token
  # Insert token and username into token store (EXPAND)
  
  Scenario: Retrieve a valid user token
    Given a user, alunduil, exists
    When I request the token for alunduil
    Then a 401 is returned with authentication details
    When I respond with proper credentials
    Then I receive a token for alunduil

