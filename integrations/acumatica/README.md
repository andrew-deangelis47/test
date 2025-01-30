# Generate API Credentials

To get access to acumatica, you need to create a client_id and client_secet
for our integration. 

1. Login to acumatica, find out which tenant/branch you should be on from customer
2. Click on more items icon, go to integration, and select show all, then click on connected applications
3. Here you can create oauth2 clients, set one up for the integration
4. The secret will be the same for sandbox/production, except the suffix, which is the tenant, ie `@Customer TEST`