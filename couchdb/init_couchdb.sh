#!/bin/bash

until curl -s http://admin:admin@couchdb:5984/_all_dbs; do
  >&2 echo "CouchDB est indisponible - attente..."
  sleep 1
done

curl -X PUT http://admin:admin@couchdb:5984/_users
curl -X PUT http://admin:admin@couchdb:5984/insulin-database
curl -X PUT http://admin:admin@couchdb:5984/_replicator
curl -X PUT http://admin:admin@couchdb:5984/_global_changes
