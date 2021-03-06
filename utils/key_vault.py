from logging import Formatter
from os import name
import config
import pandas as pd

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def retrieve_all_secrets_as_pandas(akv_uri, credential):
    client = SecretClient(vault_url=akv_uri, credential=credential)

    secrets = client.list_properties_of_secrets()
    secrets_list = [x for x in secrets]

    df = pd.DataFrame(columns=['name', 'created_on', 'content_type'])

    for secret in secrets_list:
        df = df.append({'name': secret.name, 'created_on': secret.created_on, 'content_type': secret.content_type}, ignore_index=True)

    return df

def get_secret_value(akv_uri, credential, secret_name):
    client = SecretClient(vault_url=akv_uri, credential=credential)

    secret = client.get_secret(name=secret_name)

    return secret.value

_config = config.read_config_file("variables_settings.yml")

akv_name = config.get_env_var("AKV_SERVICE_NAME", _config)
akv_uri = f"https://{akv_name}.vault.azure.net"

credential = DefaultAzureCredential()

df = retrieve_all_secrets_as_pandas(akv_uri, credential)
df = df.sort_values(by='created_on', ascending=False).head(3)

for index, row in df.iterrows():
    secret_name = row["name"]
    secret_date = row["created_on"]
    print(f"Secret name: {secret_name}. Created On: {secret_date}. Value: {get_secret_value(akv_uri, credential, secret_name)}")