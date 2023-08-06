#!/usr/bin/env python3

import click
import click_log
from .secretstores import SecretStore, SecretStoreGCP
from .factories import TokenFactory
import sys
import logging

logger = logging.getLogger(__name__)
# click_log.basic_config(logger)

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    level=logging.DEBUG,
)


# This project uses click to parse CLI arguments and
# build the command layout.
#
# The method below is the main entrypoint for the cli tool
@click.group()
@click_log.simple_verbosity_option(logger)
@click.pass_context
@click.option("--debug/--no-debug", default=False, is_flag=True)
def cli(ctx, debug):
    ctx.max_content_width = 200
    ctx.auto_envvar_prefix = "GHAK_"
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)


# The generate command is used to generate a GitHub
# or GitHub Actions runner token.
#
# You need access to a PEM file generated when the app
# was created in GitHub.
#
# The file can be read from your local disk or from GCP
# Secret manager.
@cli.command()
@click.option(
    "-i",
    "--installation-id",
    envvar="INSTALLATION_ID",
    help="App installation ID (can be found in GitHub)",
    required=True,
)
@click.option(
    "-a",
    "--app-id",
    envvar="APP_ID",
    help="GitHub application identifier (can be found in GitHub)",
    required=True,
)
@click.option(
    "-s",
    "--secret-id",
    envvar="KEY_PATH",
    help="Path to the app's private key in PEM format",
    required=True,
)
@click.option(
    "-o",
    "--owner",
    envvar="OWNER",
    help="Organization to attach runners to ",
    required=True,
)
@click.option(
    "-y",
    "--owner-type",
    envvar="OWNER_TYPE",
    help="Type of owner",
    type=click.Choice(["organization", "repo"]),
    default="organization",
    required=True,
)
@click.option(
    "-t",
    "--token-type",
    envvar="TOKEN_TYPE",
    help="Which type of token to generate",
    type=click.Choice(["runner", "github"]),
    required=True,
    default="runner",
)
def generate(installation_id, app_id, secret_id, owner, owner_type, token_type):
    # This is our main logic branc that selects between different storage mechanisms
    # Class inheritance is used to create an abstraction over the different backends
    # available to us.
    if not secret_id.startswith("gcp://"):
        secretstore = SecretStore

    elif secret_id.startswith("gcp://"):
        secret_id = secret_id.removeprefix("gcp://")

        secretstore = SecretStoreGCP

    factory = TokenFactory(installation_id, app_id, owner, owner_type, secretstore)

    factory.loadPrivateKey(secret_id)

    if token_type == "github":
        token = factory.getGitHubToken()
    elif token_type == "runner":
        token = factory.getRunnerToken()

    print(token)


# This method uploads the App's private key from
# your local disk to GCP Secret manager
@cli.command()
@click.option(
    "-f",
    "--file",
    envvar="GHA_PEM_FILE",
    help="Path to the app's private key in PEM format",
    required=True,
)
@click.option(
    "-s",
    "--secret-id",
    envvar="GHA_KEY_PATH",
    help="Path to the app's private key in PEM format",
    required=True,
)
def upload_pem(file, secret_id):
    # arguments = {"secret_id": secret_id}
    logger.info("Uploading PEM")
    # Intialze a filesystem and GCP SecretStore for getting/saving
    # the PEM file respectively
    filestore = SecretStore()
    secretmanager = SecretStoreGCP()
    # Read the PEM file
    pem_file = filestore.get(file)
    # Save the key
    secretmanager.save(secret_id, pem_file)
    logger.debug(pem_file)
