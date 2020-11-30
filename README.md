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

## Data Model/Access

### Data Object Model

#### Agency

Represents the name of a agency, available in the 'Referred Agency' field on the
new call form

**Fields**

- name: varchar(256); name of the agency

#### Call

Represents a call recorded in the new call form

**Fields**

- created_at: datetime; timestamp record was created
- updated_at: datetime; timestamp record was updated
- started_at: datetime; timestamp the call was started
- ended_at: datetime; timestamp the call was ended
- caller_name: varchar(256); the name of the caller
- caller_address: varchar(256); the caller's street address
- caller_city: varchar(256); the caller's city, part of the address
- caller_state: varchar(2); the caller's state abbreviation, part of the address
- caller_zip: varchar(5); the caller's zip code in 5 characters
- caller_number: varchar(17); the caller's phone number in the format "###-###-####"
- caller_email: varchar(); the caller's email address
- caller_dob: date; the caller's date of birth
- caller_age: int; the caller's age at the time of the call
- caller_gender: varchar(1); the caller's gender, either "M", "F", or "O" ("Other")
- caller_household_size: int; number of other individuals in the caller's household
- call_type: varchar(8), one of:
  - "INCOMING": Incoming call
  - "OUTGOING": Outgoing call
  - "FTP": Free Tax Prep (Outgoing call)
- covid_related: bool; Is this call related to COVID-19?
- client_referred: bool; Was this client referred to a provider?
- referral_id: int; ID of the referral created, if a referral was created
- referred_agency: int; Foreign Key to the Agency table
- notes: varchar(max); notes taken by the operator at the time of the call
- followup_notes: varchar(max); notes taken by the operator during call followup
- operator: int; Foreign Key to the User table, the person taking/making the call
- assigned_to: int; Foreign Key to the User table, the person assigned to follow up on this call
- call_source: varchar(max); How did you hear about the UWMS Call Center, one of:
  - "church": Church/Religious Institution
  - "work": Workplace
  - "211": LINC-211
  - "radio": Radio Ad
  - "other": Other
- duration: calculated field; duration of the call in minutes/seconds, in a string
- status: calculated field; returns the current status of the call, from CallStatus table

#### Domain (Call)

Represents a TTS domain associated with an individual call

**Fields**

- call: int; Foreign Key to the Call table
- domain: int; lookup value for the TTS Domains, one of:
  - 1: Shelter/Housing
  - 2: Employment
  - 3: Income
  - 4: Food and Nutrition
  - 5: Childcare
  - 6: Children's Education
  - 7: Adult Education
  - 8: Healthcare
  - 9: Life Skills
  - 10: Family Relationships/Social Network
  - 11: Transportation/Mobility
  - 12: Community Involvement
  - 13: Parenting Skills
  - 14: Legal
  - 15: Mental Health
  - 16: Substance Abuse
  - 17: Safety
  - 18: Disability Services
  - 19: Credit/Financial Management
  - 20: Spirituality
- label: calculated field; returns the string label for the domain number

#### CallStatus

Indicates a status for a call at a given point in time

**Fields**

- created_at: datetime; timestamp record was created
- call: int; Foreign Key to the Call table
- status: int; value indicating the call status, one of:
  - 1: CONTACTED
  - 2: REFERRED
  - 3: INFO
  - 4: CLOSED
- label: calculated field; returns the string label for the status

#### Request

Represents a request made through the online request form

**Fields**

- created_at: datetime; timestamp record was created
- updated_at: datetime; timestamp record was updated
- contact: varchar(200); the name of the person making the request
- email: varchar; email address for the person making the request
- primary_phone: varchar(17); callback number for the person making the request, in the format "###-###-####"
- secondary_phone: varchar(17); optional backup number for the person making the request, in the format "###-###-####"
- add_info: varchar(max); additional notes field associated with the request
- confirmation_code: varchar(8); lookup value (along with primary_phone) for clients to check the status of their request
- referral_id: int; if a referral is made from this request, the referral ID
- status: calculated field; the current status of this request

#### Domain (Request)

Represents a TTS domain associated with an individual request

**Fields**

- request: int; Foreign Key to the Request table
- domain: int; lookup value for the TTS Domains, one of:
  - 1: Shelter/Housing
  - 2: Employment
  - 3: Income
  - 4: Food and Nutrition
  - 5: Childcare
  - 6: Children's Education
  - 7: Adult Education
  - 8: Healthcare
  - 9: Life Skills
  - 10: Family Relationships/Social Network
  - 11: Transportation/Mobility
  - 12: Community Involvement
  - 13: Parenting Skills
  - 14: Legal
  - 15: Mental Health
  - 16: Substance Abuse
  - 17: Safety
  - 18: Disability Services
  - 19: Credit/Financial Management
  - 20: Spirituality
- label: calculated field; returns the string label for the domain number

#### Response

Represents a response by a DTD staff to a request

**Fields**

- request: int; Foreign Key to the Request table
- created_at: datetime; timestamp of record creation
- created_by: int; Foreign Key to the User table, the user who created the response
- status: varchar(9); the status associated with the response, one of:
  - PENDING: Pending
  - RECEIVED: Received
  - REVIEWED: Under Review
  - CONTACTED: Contact Pending
  - REFERRED: Referred
  - CLOSED: Closed
- note: varchar(max); update note associated with the response, visible to the client

### Database Access

Once deployed, the database can be accessed through the Adminer interface using the following values:

- URL: db.call.drivingthedream.org
- Server: postgres
- Username: admin
- Password: POSTGRES_PASSWORD in ‘.env’ file stored on the server
- Database: dtd_request

### Reports/Views

There are a number of reports/views included in the running database as well. Note, these were created using the Adminer interface and are not associated with the application code in any way. This means that, in the event of database loss, these tables will need to be re-created directly in the database and will not be automatically built.

#### Calls by Age

Description: For all time, the number of calls by caller age.
Table Name: calls_by_age
SQL:

```sql
   SELECT
        CASE
            WHEN (dtd_calls_call.caller_age < 18) THEN '< 18'::text
            WHEN (dtd_calls_call.caller_age < 30) THEN '18 - 29'::text
            WHEN (dtd_calls_call.caller_age < 40) THEN '30 - 39'::text
            WHEN (dtd_calls_call.caller_age < 50) THEN '40 - 49'::text
            WHEN (dtd_calls_call.caller_age < 60) THEN '50 - 59'::text
            WHEN (dtd_calls_call.caller_age < 70) THEN '60 - 69'::text
            WHEN (dtd_calls_call.caller_age < 80) THEN '70 - 79'::text
            WHEN (dtd_calls_call.caller_age >= 80) THEN '80+'::text
            ELSE 'None Listed'::text
        END AS age_category,
    count(*) AS calls
   FROM dtd_calls_call
  GROUP BY
        CASE
            WHEN (dtd_calls_call.caller_age < 18) THEN '< 18'::text
            WHEN (dtd_calls_call.caller_age < 30) THEN '18 - 29'::text
            WHEN (dtd_calls_call.caller_age < 40) THEN '30 - 39'::text
            WHEN (dtd_calls_call.caller_age < 50) THEN '40 - 49'::text
            WHEN (dtd_calls_call.caller_age < 60) THEN '50 - 59'::text
            WHEN (dtd_calls_call.caller_age < 70) THEN '60 - 69'::text
            WHEN (dtd_calls_call.caller_age < 80) THEN '70 - 79'::text
            WHEN (dtd_calls_call.caller_age >= 80) THEN '80+'::text
            ELSE 'None Listed'::text
        END
  ORDER BY
        CASE
            WHEN (dtd_calls_call.caller_age < 18) THEN '< 18'::text
            WHEN (dtd_calls_call.caller_age < 30) THEN '18 - 29'::text
            WHEN (dtd_calls_call.caller_age < 40) THEN '30 - 39'::text
            WHEN (dtd_calls_call.caller_age < 50) THEN '40 - 49'::text
            WHEN (dtd_calls_call.caller_age < 60) THEN '50 - 59'::text
            WHEN (dtd_calls_call.caller_age < 70) THEN '60 - 69'::text
            WHEN (dtd_calls_call.caller_age < 80) THEN '70 - 79'::text
            WHEN (dtd_calls_call.caller_age >= 80) THEN '80+'::text
            ELSE 'None Listed'::text
        END;
```

#### Calls by Gender

Description: For all time, the number of calls by caller gender
Table Name: calls_by_gender
SQL:

```sql
   SELECT dtd_calls_call.caller_gender,
      count(*) AS calls
      FROM dtd_calls_call
   GROUP BY dtd_calls_call.caller_gender
   ORDER BY dtd_calls_call.caller_gender;
```

#### Calls by Zip

Description: For all time, the number of calls by caller zip code
Table Name: calls_by_zip
SQL:

```sql
   SELECT dtd_calls_call.caller_zip,
      count(*) AS calls
   FROM dtd_calls_call
   GROUP BY dtd_calls_call.caller_zip
   ORDER BY dtd_calls_call.caller_zip;
```

#### Weekly Counts

Description: By week, the number of all requests (incoming calls + online requests), incoming calls, online requests, and the number of each that is associated with a referral.
Table Name: weekly_counts
SQL:

```sql
   SELECT calls.week,
    (calls.calls + online_requests.online_requests) AS all_requests,
    (calls.calls_referred + online_requests.online_requests_referred) AS all_requests_referred,
    calls.calls,
    calls.calls_referred,
    online_requests.online_requests,
    online_requests.online_requests_referred
   FROM (
      (
         SELECT (date_trunc('week'::text, (dtd_calls_call.created_at - '05:00:00'::interval)))::date AS week,
            count(*) AS calls,
            count(CASE WHEN dtd_calls_call.client_referred THEN 1 ELSE NULL::integer END) AS calls_referred
         FROM dtd_calls_call
         WHERE ((dtd_calls_call.call_type)::text = 'Incoming'::text)
         GROUP BY ((date_trunc('week'::text, (dtd_calls_call.created_at - '05:00:00'::interval)))::date)
         ORDER BY ((date_trunc('week'::text, (dtd_calls_call.created_at - '05:00:00'::interval)))::date)
      ) calls
      LEFT JOIN (
        SELECT (date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date AS week,
            count(*) AS online_requests,
            sum(CASE WHEN req.referred THEN 1 ELSE NULL::integer END) AS online_requests_referred
         FROM (
            SELECT req_1.created_at,
               req_1.id,
               (sum(CASE WHEN ((res.status)::text = 'REFERRED'::text) THEN 1 ELSE 0 END) > 0) AS referred
               FROM (
                  dtd_request_request req_1
                  LEFT JOIN dtd_request_response res ON ((req_1.id = res.request_id)))
                  GROUP BY req_1.id
               ) req
          GROUP BY ((date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date)
          ORDER BY ((date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date)
      ) online_requests
      ON ((calls.week = online_requests.week))
   );
```

#### Weekly Domain Counts

Description: By week and domain, the number of all requests (incoming calls + online requests), incoming calls, online requests, and the number of each that is associated with a referral.
Table Name: weekly_counts
SQL:

```sql
   SELECT COALESCE(calls.week, online_requests.week) AS week,
      COALESCE(calls.label, online_requests.label) AS domain,
      (COALESCE(calls.calls, (0)::bigint) + COALESCE(online_requests.online_requests, (0)::bigint)) AS all_requests,
      (COALESCE(calls.calls_referred, (0)::bigint) + COALESCE(online_requests.online_requests_referred, (0)::bigint)) AS all_requests_referred,
      COALESCE(calls.calls, (0)::bigint) AS calls,
      COALESCE(calls.calls_referred, (0)::bigint) AS calls_referred,
      COALESCE(online_requests.online_requests, (0)::bigint) AS online_requests,
      COALESCE(online_requests.online_requests_referred, (0)::bigint) AS online_requests_referred
   FROM (
      (
         SELECT (date_trunc('week'::text, (call.created_at - '05:00:00'::interval)))::date AS week,
            domain_mapping.label,
            count(*) AS calls,
            count(CASE WHEN call.client_referred THEN 1 ELSE NULL::integer END) AS calls_referred
         FROM ((dtd_calls_call call
            LEFT JOIN dtd_calls_domain domain ON ((call.id = domain.call_id)))
            LEFT JOIN domain_mapping ON ((COALESCE(domain.domain, 0) = domain_mapping.id)))
         WHERE ((call.call_type)::text = 'Incoming'::text)
         GROUP BY ((date_trunc('week'::text, (call.created_at - '05:00:00'::interval)))::date), domain_mapping.label
         ORDER BY ((date_trunc('week'::text, (call.created_at - '05:00:00'::interval)))::date), domain_mapping.label
      ) calls
      FULL JOIN (
         SELECT (date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date AS week,
            domain_mapping.label,
            count(*) AS online_requests,
            sum(CASE WHEN req.referred THEN 1 ELSE NULL::integer END) AS online_requests_referred
            FROM (
               (
                  (
                     SELECT req_1.created_at,
                        req_1.id,
                        (sum(CASE WHEN ((res.status)::text = 'REFERRED'::text) THEN 1 ELSE 0 END) > 0) AS referred
                     FROM (
                        dtd_request_request req_1
                        LEFT JOIN dtd_request_response res ON ((req_1.id = res.request_id))
                     )
                     GROUP BY req_1.id
                  ) req
                  LEFT JOIN dtd_request_domain domain ON ((req.id = domain.request_id))
               )
               LEFT JOIN domain_mapping ON ((COALESCE(domain.domain, 0) = domain_mapping.id))
            )
            GROUP BY ((date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date), domain_mapping.label
            ORDER BY ((date_trunc('week'::text, (req.created_at - '05:00:00'::interval)))::date), domain_mapping.label
      ) online_requests
      ON (((calls.week = online_requests.week) AND ((calls.label)::text = (online_requests.label)::text)))
   );
```

## Deployment

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
