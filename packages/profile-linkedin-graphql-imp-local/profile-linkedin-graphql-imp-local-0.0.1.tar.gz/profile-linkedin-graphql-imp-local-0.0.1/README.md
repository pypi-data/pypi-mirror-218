# LinkedIn Profile Importer

The LinkedIn Profile Importer is a program that allows you to import profiles from the LinkedIn API and enter them into the Circles database.

## Prerequisites

Before running this program, you need to have the following:

- A LinkedIn Developer account to create a LinkedIn app. You can create a new app by [following this link](https://www.linkedin.com/developers/apps/new).
- Database credentials (username and password) for the database.

## How to Run Locally

To run the program locally, follow these steps:

1. Create a LinkedIn app:
   - Go to the [LinkedIn Developer portal](https://www.linkedin.com/developers/apps) and create a new app.
   - Set the app name to "YOUR_APP_NAME" and associate it with "Circles.ai".
   - Set the Redirect URI.
   - Verify the app to be associated with the company.
   - Add the product "Sign In with LinkedIn using OpenID Connect".
   - Open the permissions tab and enable the following scopes: "openid", "profile", and "email".
   -enter your access token to .env file


2. Configure the database:
   - Update the `.env` file with your database username and password in the following format:
     RDS_HOSTNAME=host_name
     RDS_USERNAME=your_database_username
     RDS_PASSWORD=your_database_password


3. Implement Member (3-legged) authorization:
   - Once the app is set up and running, you need to implement Member authorization to retrieve access tokens.
   - Use the authorization code obtained from LinkedIn and pass it to the `getProfile.addAccessToken(self, access token)` function. This function will add the access token to the environment and add his details to the db.

4. Run the program:
   - Open a terminal or command prompt.
   - Navigate to the project directory.
   - Execute the program using `python src.run.py`.

## Running the YAML Workflow

To run the program using the provided YAML workflow, follow these steps:

1. Create a LinkedIn app and implement Member (3-legged) authorization as mentioned in the "How to Run Locally" section above.

2. Retrieve the User Access Token:
   - Use the implemented authorization flow to obtain the User Access Token from LinkedIn.
   - Make sure to copy the User Access Token for use in the next step.

3. Set up the GitHub Secrets:
   - Go to your GitHub repository's page.
   - Click on the "Settings" tab.
   - In the left sidebar, click on "Secrets".
   - Click on the "New repository secret" button.
   - Enter the secret name as "LINKEDIN_API_TOKEN".
   - Paste the User Access Token copied from the previous step as the secret value.

4. Push your code changes:
   - Commit your updated code with the YAML file and push it to your repository.

5. GitHub Workflow:
   - The provided YAML workflow will automatically trigger when you push your code changes.
   - The workflow will run the program using the LinkedIn API User Access Token stored in the secret.
   - The program will retrieve user data from the LinkedIn API and import it into the Circles database.

