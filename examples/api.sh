#!/bin/bash

# Create an User
curl -v -X PUT http://api.margarine.raxsavvy.com/v1/users/${USERNAME} -F "email=username@example.com"

# Read an User
curl -v -X GET http://api.margarine.raxsavvy.com/v1/users/${USERNAME}

# Update an User
curl -v -X PUT http://api.margarine.raxsavvy.com/v1/users/${USERNAME} -F "name=Fabio Lanzoni" -H "X-Auth-Token: 1e13e9e5-445b-4509-a8a4-bb4a1657f431"

# Delete an User
curl -v -X DELETE http://api.margarine.raxsavvy.com/v1/users/${USERNAME} -H "X-Auth-Token: 1e13e9e5-445b-4509-a8a4-bb4a1657f431"


# Create an Article
curl -v -X POST http://api.margarine.raxsavvy.com/v1/articles/ -F "url=http://developer.rackspace.com/blog/a-look-back-at-pycon-australia-2013.html"

# Read an Article
curl -v -X GET http://api.margarine.raxsavvy.com/v1/articles/7d7dae0b-2ed6-53ed-a1c5-5b1245e0f397

# Update an Article
# Updates will be handled automatically by the backend parsing system.

# Delete an Article
# Deletes will be handled automatically by the backend parsing system.


# User Authentication
curl -v -X GET --digest -u ${USERNAME} http://api.margarine.raxsavvy.com/v1/users/${USERNAME}/token

