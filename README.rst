.. image:: https://travis-ci.org/squirrelo/MovieNightBot.svg?branch=develop
    :target: https://travis-ci.org/squirrelo/MovieNightBot

Movie Night Bot
---------------
A simple discord bot that tracks movie suggestions, watched movies, and runs votes on what movie to watch form the suggestions list.
Includes weighted-choice voting, tie runoff logic, and the ablity to turn off suggestion capability if users are getting too rowdy.

Running the bot
---------------
1) Create a `config.yaml` based on the config-example.yaml in this repo.
2) Start the server using the command `python -m movienightbot -c /path/to/config.yaml`  You can optionally also pass `-f /path/to/file.log` to set where the log file should be written.

Planned Features
 * Block specific people from suggesting on a server
 * Paginate the watched and suggested so you can scroll through with reactions

Contributing
------------
`flake8
<https://flake8.pycqa.org/en/latest/>`_ and `black
<https://black.readthedocs.io/en/stable/>`_  standards are enforced for all pull requests.
