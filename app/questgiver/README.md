# Memphis | How Can I Help?

Originally prepared as a response to the need to advertise community needs and allow
community members to pick up these requests and act on them in a distributed fashion.
This application is divided into multiple sections:

## Home Screen

Displays a list of requests, called 'opportunities', that have been posted and approved.
A community member may view and/or accept a request on this page, whereupon they are
sent an e-mail with follow-up information.

### Review an Opportunity

Allows an un-authenticated user to review a request from the home screen and accept the
request. To accept, the user must provide their email address and phone number for 
contact information.

## Post an Opportunity

Web form to generate a new request. Requests must be approved before they are posted to
the home screen by an authenticated user. Requests must include:

- A contact person for the request
- - Name
- - Email Address
- - Phone Number
- A short description, or 'topic'
- A priority (used to help determine sort order on the home screen)
- Number of days to allow for this request
- A longer form description

## Manage Requests (Authenticated)

When an approved user logs in, they have access to this drop-down menu on the navigation
bar with the following options:

### Pending Approval (Authenticated)

Allows an authenticated user to review, modify, reject, or approve a submitted request.
Approved requests are posted to the home screen.

### Overdue Tasks (Authenticated)

A list of accepted requests that have not been completed and have been accepted longer
than the number of days originally allows. The authenticated user may reach out to the
person who accepted the request to determine status and/or choose to reject, modify, or
repost the request. Reposted requests are given priority in the sort order on the home
screen.

### Completed Tasks (Authenticated)

A list of completed requests for review by authenticated users.

## Admin Interface

The default Django admin interface, found at HOSTNAME/admin. Typically only used by 
superusers to assign additional user accounts. Currently, any authenticated user has
access to the authenticated screens/views, no need to mark them as staff or superusers.