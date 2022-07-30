#!/bin/bash

cd ../Docker

docker build -t vikrampruthvi5/base-ubuntu-python .

# push docker image to docker hub
docker login -u vikrampruthvi5 -p dckr_pat_1UOqWgyCt18XCKIawZU4EfsD3tE
docker push vikrampruthvi5/base-ubuntu-python