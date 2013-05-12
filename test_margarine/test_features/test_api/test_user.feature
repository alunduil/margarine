# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

Feature: Interact with Margarine's User API
  In order to verify that the user's API functions correctly, we'll run various
  requests against it.

  Scenario: Retrieve a known user that does not exist
    Given that I have a username, alunduil
    When I request its information
    Then I receive a 404 Not Found

  Scenario: Retrieve a known user that does exist without a token
    Given that I have a username alunduil
    When I request its information
    Then I receive a 401 Not Authorized

  Scenario: Log in to the web service
    Given that I have an existing username alunduil
    When I request the user's token
    Then I receive a 401 Not Authorized
    # TODO Add remaining steps.
    
  Scenario: Create a new user that already exists
    Given that I have an existing username alunduil
    When I try to create that user
    Then I receive a 401 Not Authorized

  Scenario: Create a nwe user that does not already exist
    Given that I have an username alunduil
    When I request creation of the user
    Then I receive a 202 Accepted
    And I can see the user in the database

