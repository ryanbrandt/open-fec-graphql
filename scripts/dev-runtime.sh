#!/bin/bash

export FLASK_APP=app/app.py 
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run