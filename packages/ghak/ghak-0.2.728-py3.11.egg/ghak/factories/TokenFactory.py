import time
import jwt
import json
import requests
import logging

logger = logging.getLogger(__name__)


class TokenFactory:
    GITHUB_API_VERSION = "2022-11-28"
    GITHUB_REQUEST_CONTENTTYPE = "application/vnd.github+json"
    installations_url = "https://api.github.com/app/installations"

    HEADERS = {
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
        "Accept": GITHUB_REQUEST_CONTENTTYPE,
    }

    def __init__(self, installation_id, app_id, owner, owner_type, secretstore):
        self.secretstore = secretstore()
        self.installation_id = installation_id
        self.app_id = app_id
        self.owner = owner
        self.private_key = ""

        if owner_type == "organization":
            self.runner_url = "https://api.github.com/orgs"
        elif owner_type == "repo":
            self.runner_url = "https://api.github.com/repos"

    def loadPrivateKey(self, secret_id):
        logger.debug("Loading private key")
        self.secretstore.get(secret_id)
        try:
            self.private_key = self.secretstore.secrets[secret_id].encode("UTF-8")
        except Exception as e:
            logger.error(e)
            raise

    def getEncodedJWT(self):
        # GitHub only permits tokens to be valid for a maximum time period of 600s
        #
        logger.debug("Building encoded JWT with following payload:")
        payload = {
            # Issued at time
            "iat": int(time.time()),
            # JWT expiration time (10 minutes maximum)
            "exp": int(time.time()) + 600,
            # GitHub App's identifier
            "iss": self.app_id,
        }
        logger.debug(payload)
        signing_key = jwt.jwk_from_pem(self.private_key)

        # Create JWT
        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")
        logger.debug("Created encoded JWT:")
        logger.debug(encoded_jwt)

        return encoded_jwt

    def getGitHubToken(self):
        # Get a JWT to use for authorization on subsequent request
        encoded_jwt = self.getEncodedJWT()
        # Add JWT to global class headers
        headers = self.HEADERS
        headers["Authorization"] = f"Bearer {encoded_jwt}"
        auth_url = f"{self.installations_url}/{self.installation_id}/access_tokens"
        # Retrieve a GitHub token
        logger.debug("Requesting access token at {}".format(auth_url))
        logger.debug("Headers: {}".format(headers))
        try:
            token_object = json.loads(requests.post(headers=headers, url=auth_url).text)
        except Exception as e:
            logger.error(e)
            raise
        github_token = token_object["token"]

        result = github_token
        logger.debug("Received token: {}".format(result))
        return result

    def getRunnerToken(self):
        # A valid "github" token is required to request a runner token
        logger.debug("Beginning GitHub Token request...")
        github_token = self.getGitHubToken()

        headers = self.HEADERS
        logger.debug("Beginning runner registration token request...")
        headers["Authorization"] = "Bearer {}".format(github_token)
        token_url = f"{self.runner_url}/{self.owner}/actions/runners/registration-token"

        token_object = json.loads(requests.post(headers=headers, url=token_url).text)

        registration_token = token_object["token"]
        result = registration_token
        logger.debug(f"Received registration token: {result}")

        return result
