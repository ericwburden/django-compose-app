# Driving the Dream Call Center

This project contains the source code for the DTD Call Center application. This
application supports both online requests entered by potential clients seeking
services and recording call data (in an online form) by call center operators.
The application also supports follow-up on calls and online requests.

## Call Center Interface/Screens

### Home Screen

![Home Screen](/screenshots/home-screen.jpg?raw=true)

After submitting the request, the client will be taken to a confirmation screen
with a confirmation code. The client can use that code, with the phone number
they entered into the request form, at the "View My Requests" link to check the
status of their request. The client will also receive an automated email once
their request is submitted and each time their request is updated.

### Check Request Status

![Check Status Form](/screenshots/check-status-form.png?raw=true)

Clients can use this form to check the current status of their request.

### Logged In Home Screen

![Logged In Home Screen](/screenshots/logged-in-home-screen.png?raw=true)

1. Link to manage online requests
2. Link to enter a new call form
3. Link to review recorded call forms
4. Link to review data reports

### Manage Requests Screen

![Manage Requests Screen](/screenshots/manage-requests-screen.png?raw=true)

1. The name of the individual who entered the request into the online request
   form; clicking the contact name will expand the entry to reveal additional
   information about the request.
2. The corresponding TTS domain, 'Multiple' if multiple domains were chosen.
3. The date the request was last updated.
4. The current request status, clicking the current status will display a
   menu of available statuses to update to. Depending on the new status, an
   additional form may be displayed. Closed requests will no longer appear on
   this menu.
5. The operator who has 'claimed' this request and is responsible for following
   up with the client.

The results on this screen are paged. Requests that require no further action
should be closed.

### New Call Form

![New Call Form](/screenshots/new-call-form.png?raw=true)

1. The operator should click the 'Set' button in the 'Call Started' field
   when answering or initiating a call.
2. The operator should click the 'Set' button in the 'Call Ended' field
   when hanging up a call.
3. The type of call may be either:
   - Incoming Call: for calls answered by a call center operator
   - Outgoing Call: for calls placed by a call center operator
   - Free Tax Prep (Outgoing): for calls placed by a call center operator for
     Free Tax Prep services
4. If a referral was made through the DTD network at the time of the call,
   the operator should check 'Was this client referred to a provider?' and enter
   the relevant referral information.

### Review Calls Screen

![Review Calls Screen](/screenshots/review-calls-screen.png?raw=true)

1. An entry in the calls list. Each entry can be clicked to display an expanded
   form as shown containing additional information and controls.
2. The 'Update' button displays an update form for the call, allowing an
   operator to update call information and follow-ups.
3. The 'Direct Link' button displays a read-only version of the call
   information. This button provides a link that is suitable to be shared
   internally for troubleshooting or requests for assistance.

### Reports Screen

![Reports Screen](/screenshots/reports-screen.png?raw=true)

Displays pre-configured reports on call center activity, including:

1. Calls Per Day: The number of calls per day per type.
2. Call Duration per Day: The time (in minutes) spent on calls per day per type.
3. Requests by Domain: The relative number of incoming requests (via the
   online requests form) by domain for the top five domains. Requests are counted
   in each indicated domain.
4. Calls Referred: The overall percentage of all calls referred (all types).
5. Intakes by Type: The number of total intakes by type (Incoming Calls v.
   Online Requests)
6. Weekly Report: Provides a downloadable data table indicating the number
   of incoming calls, incoming calls referred, online requests, and online
   requests referred per domain per week.

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

- [Docker](https://docs.docker.com/) - Containers!
- [Docker Compose](https://docs.docker.com/compose/) - Container orchestration
- [Python 3.6](https://www.python.org/downloads/release/python-360/) - The (primary) language

## Container Services Included

- [Django](https://www.djangoproject.com/) - The web framework used
- [Traefik](https://containo.us/traefik/) - Load balancer, reverse proxy, and SSL certificate management
- [Nginx](https://www.nginx.com/) - Static file server
- [PostgreSQL](https://www.postgresql.org/) - Backend database
- [docker-autoheal](https://hub.docker.com/r/willfarrell/autoheal/) - Monitor and restart unhealthy docker containers

## Authors

- **Eric Burden** - _Initial work_ - [My Site](https://ericburden.work)

See also the list of [contributors](https://github.com/ericwburden/django-compose-app/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- All the Traefik tutorials and documentation
- DigitalOcean, for the various tutorials I researched for this project
- My family for putting up with me while I worked on this
