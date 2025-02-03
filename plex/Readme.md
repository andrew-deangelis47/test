## Generate API Credentials

In order to get API access to Plex do the following:

1. Get a user account to the customer's Plex account.
2. Get developer access so that you can login to the developer portal (https://new.developers.plex.com/)
3. Login to the developer site
4. On the top banner there should appear a "My Applications" menu item. Click "My Applications"
5. "Add" a new application, set name (e.x. paperless_parts_integration), and select Products > Common APIs
6. The new application will now show a Consumer Key and Secret Key.
7. Add the Consumer Key to the api_key field of the PLEX section of the secrets file
8. The api key is the same between test & production. Only the url needs to change to access one or the other. a. Test
   URL: base_url=https://test.connect.plex.com
   b. Prod URL: base_url=https://connect.plex.com

## Data Sources

There are multiple possible data sources for use in PLEX. The preferred method is the open API, which is under active
development and still supported. All other connection methods are not officially supported by PLEX.

When needed, the ODBC connection can be used to pull data, but it cannot push data back into PLEX. The server it
connects to is mere a staging area for reporting data this refreshed every four hours.

For more information on data sources
see: https://docs.google.com/document/d/1vfYDn0m1skkwdQDGyHkaWpekTrwh60aV2NfEfbSmgzg/edit?usp=sharing

## Classic vs UX

Classic and UX are just different interfaces to the same cloud hosted database. UX has deprecated several fields and
features from Classic, but is otherwise operating off the same data. If you use the API to write data into PLEX it
should be visible in both Classic and UX.

Plex does not have an end of life date for Classic, and is trying to migrate users slowly over time. We will have to
support both in our integrations, though the difference may not be significant to us since it is the same API.


