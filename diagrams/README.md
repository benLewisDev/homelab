# Diagrams

## Overview

This is the directory used to store and work on code that generates the diagrams requied for me to architect my homelab set up

## Prequisites

- Python 3.7 or higher
- pip
- Graphviz

## Set Up

1. Install Graphviz and Pip
   `sudo dnf install python3-pip graphviz`
2. check that Graphviz installed. (Dot is the graphviz engine)
   `dot --version`
3. Check pip installed
   `pip --version`
4. create virtual environment
   `python3 -m .venv venv/`
5. Initiate virtual environment
   `source .venv/bin/activate`
6. Install requirements.txt
   `pip -r install requirements.txt`
7. Profit?

## Refernce Documentation
- Diagrams documentation - [Diagrams](https://diagrams.mingrammer.com/docs/getting-started/installation) 
- Icons found here - [Self Hosted icons](https://selfh.st/icons/) 
