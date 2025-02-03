## Developing Business Central Extensions

In order to expose all necessary data through the Business Central [OData API](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/webservices/odata-web-services), we have created a Business Central [extension](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-dev-overview). The source code for it is located primarily in `al_extension/PageExtensions.al`.

To get started developing this extension, follow [this guide](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-get-started). In summary:

1. Download VS Code

2. Download the AL Language extension

3. Open the `al_extension` directory

4. Press Cmd+Shift+P --> AL: Download Symbols

5. Modify `PageExtensions.al` as necessary

6. Press Ctrl+F5 to deploy the extension to the customer's Sandbox environment
