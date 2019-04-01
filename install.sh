#!/bin/bash

# install pip
sudo easy_install pip

# install virtualenv
sudo pip install virtualenv

# create a new virtualenv
virtualenv twelve_env

# open the virtualenv
source twelve_env/bin/activate

# install dependencies
sudo pip install -r requirements.txt

# done
echo "Finished installation! :)"
