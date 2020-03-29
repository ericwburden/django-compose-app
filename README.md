# Project Title

This project makes it quick and simple to develop a docker-composed Django application
locally and deploy to a remote server for production use. The default application is a
web-based request and response platform.

## Getting Started

To begin development on this project, add your environment variables by running
`./env.sh dev` and filling in the variable values by following the instructions. 
Then simply run `./deploy.sh dev` to spin up a collection of docker files. 
`./deploy.sh -h` displays the help file for the deployment script, `./deploy.sh -c` 
cleans up the build files (don't use this unless you don't like using the 
`docker-compose down` command...).

### Prerequisites

You'll need a working Docker and Docker Compose installation to use this project, as
well as an installation of Python3.6+.

### Remote Deployment

To deploy to a remote server, ensure that the server HOSTNAME, traefik.HOSTNAME, and
db.HOSTNAME all have A records that point to the server's IP and that you've filled in 
the prod environment variables (use `./env.sh prod`).

Copy the application folder to the remote server using `scp -r $PWD user@hostname:dest_folder` 
from inside the project directory (or `git clone` if that's your speed). Log into the 
remote server via SSH, navigate to the destination folder, and run `./deploy.sh prod -b`. 
Give it 30 seconds or so to establish container health, and you're off to the races.

## Sample Application

Deployed as-is, the application produces a web-based request and response platform. You 
can learn more about using that application [HERE](app/questgiver/README.md)

## Built With

* [Docker](https://docs.docker.com/) - Containers!
* [Docker Compose](https://docs.docker.com/compose/) - Container orchestration
* [Python 3.6](https://www.python.org/downloads/release/python-360/) - The (primary) language

## Container Services Included

* [Django](https://www.djangoproject.com/) - The web framework used
* [Traefik](https://containo.us/traefik/) - Load balancer, reverse proxy, and SSL certificate management
* [Nginx](https://www.nginx.com/) - Static file server
* [PostgreSQL](https://www.postgresql.org/) - Backend database
* [docker-autoheal](https://hub.docker.com/r/willfarrell/autoheal/) - Monitor and restart unhealthy docker containers

## Authors

* **Eric Burden** - *Initial work* - [My Site](https://ericburden.work)

See also the list of [contributors](https://github.com/ericwburden/django-compose-app/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* All the Traefik tutorials and documentation
* DigitalOcean, for the various tutorials I researched for this project
* My family for putting up with me while I worked on this

