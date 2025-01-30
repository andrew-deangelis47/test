## Testing
`pytest integrations/mietrak_pro --cov=integrations/mietrak_pro`

To get a coverage report, you can add the argument `--cov-report html` to the above command.


`flake8 ./integrations --config=integrations/.flake8.ini`

## New Builds (Dec 2024) 

### Notes:
* The following serves as a reference for a new build system developed for any integrations built AFTER Dec 2024
    * All older integrations can be grandfathered into this build system over time
    * See https://paperlessparts.atlassian.net/wiki/spaces/ENGINEERIN/pages/1342275590/Integrations+Release+Process+Current+and+Future for more information
* Useful reference docs:
    * Docker buildx
        * https://docs.docker.com/reference/cli/docker/buildx/
    * Docker buildx bake
        * https://docs.docker.com/reference/cli/docker/buildx/bake/
    * PR with more info and discussion
        * https://bitbucket.org/paperlessparts/integrations/pull-requests/969
* These new builds depend on access to cicd.paperlessparts.com
    * To request access, create an IT ticket
        * Request access to the prod jenkins IT role
        * Once granted, log in via Okta

### Repo structure notes
* All customer-specific code lives in the customers directory 
    * e.g. customers/example_customer

* All ERP system specific code lives in the erp_systems directory
    * e.g. erp_systems/hubpsot

### Adding a new integration
* For a new customer integration build, add a new `target` block to `docker-bake.hcl`
    * Example (note `CUSTOMER` and `ERP_SYSTEM` and `HTTP_PORT`): 
    * The `HTTP_PORT` is the port needed to be exposed by the container in order to receive traffic from the `API Gateway`. It will be specified in the Keeper record that also specifies the API Gateway Path.
        ```
        target "customer-example_customer" {
            contexts = {
                base = "target:base"
            }
            dockerfile = "Dockerfile.cicd"
            target = "customer"
            args = {
                CUSTOMER = "example_customer",
                ERP_SYSTEM = "hubspot",
                HTTP_PORT = "1024",
                PURPOSE = BUILD_ID != "" ? "release" : "development",
            }
            tags = [
                BUILD_ID != "" ? "${REGISTRY}/integrations/customers/example_customer:${BUILD_ID}" : "",
                BUILD_ID == "" ? "integrations/customers/example_customer:development" : "",
                DEPLOY == "true" ? "${REGISTRY}/integrations/customers/example_customer:release" : "",
            ]
            annotations = BUILD_ANNOTATIONS
            platforms = [
                "linux/amd64"
            ]
        }

        ```

### Running builds on cicd.paperlessparts.com
* Rebuild the base integration at https://cicd.paperlessparts.com/job/Integrations/job/build_base_integration/

* Build a new customer integration at https://cicd.paperlessparts.com/job/Integrations/job/build_integration/
    * Must select a `CUSTOMER` from dropdown list
    * Can use the `NONMASTER_DEPLOY` param to deploy an image off of a feature branch if needed

### Running dev builds locally
* Local commands to mimic the jenkins jobs above:
    * Build base integration: `docker buildx bake`
    * Build customer integration: `docker buildx bake <target>`
        * e.g. `docker buildx bake customer-example_customer`
    