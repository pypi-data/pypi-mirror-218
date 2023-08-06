import logging

logger = logging.getLogger(__name__)


class SecretStore:
    def __init__(self, **kwargs):
        self.jwt = ""
        self.secrets = {}

    def save(self, secret_id, secret):
        self.secrets[secret_id] = secret
        return secret

    def get(self, filepath):
        secret = ""
        try:
            with open(filepath, "r") as pem_file:
                secret = pem_file.read()
            self.secrets[filepath] = secret
        except Exception as e:
            logger.error(e)
            raise

        return secret


class SecretStoreGCP(SecretStore):
    def __init__(self, **kwargs):
        self.secrets = {}

        import google.auth
        import google.api_core.exceptions

        from google.cloud import secretmanager

        try:
            _, self.project_id = google.auth.default()
            self.client = secretmanager.SecretManagerServiceClient()

        except google.auth.exceptions.DefaultCredentialsError:
            self.project_id = None

    def __check_secret_existance(self, secret_id):
        # Adding data to a secret in SecretManager is a two step process
        # First the secret must be created. Once the secret is created
        # a new version containing the secret's data may be added.
        #
        # This internal method checks for the existance of the secret
        # located at `secret_id` and if it is not found, creates it.
        self.gcloud_secret_name_path = (
            f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        )
        try:
            payload = self.client.access_secret_version(
                name=self.gcloud_secret_name_path
            ).payload.data.decode("UTF-8")
            return True
        except google.api_core.exceptions.NotFound:
            # Build the resource name of the parent project.
            parent = f"projects/{self.project_id}"

            # Build a dict of settings for the secret
            secret = {"replication": {"automatic": {}}}
            logger.debug(
                "No secret found with the specified ID, creating a secret now."
            )
            # Create the secret
            response = self.client.create_secret(
                secret_id=secret_id, parent=parent, secret=secret
            )
            parent = self.client.secret_path(self.project_id, secret_id)
            response = self.client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {"data": "placeholder".encode("UTF-8")},
                }
            )
            # Print the new secret name.
            logger.debug(f"Created secret: {response.name}")
            return True

        except Exception as e:
            logger.error(e)
            raise

    def save(self, secret_id, secret):
        # Create the Secret Manager client.
        self.__check_secret_existance(secret_id)
        parent = self.client.secret_path(self.project_id, secret_id)

        # Make the request
        try:
            response = self.client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {"data": secret.encode("UTF-8")},
                }
            )
            logger.debug(response)
            logger.debug("save succesful")
        except Exception as e:
            logger.error(e)
            raise
        # Handle the response

        return secret.encode("UTF-8")

    def get(self, secret_id):
        gcloud_secret_name_path = (
            f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        )
        response = self.client.access_secret_version(name=gcloud_secret_name_path)

        self.secrets[secret_id] = response.payload.data.decode("UTF-8")
        return response.payload.data.decode("UTF-8")
