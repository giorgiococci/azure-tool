import config
import pandas as pd

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def retrieve_all_secrets_as_pandas(akv_uri, credential):
    client = SecretClient(vault_url=akv_uri, credential=credential)

    secrets = client.list_properties_of_secrets()
    secrets_list = [x for x in secrets]

    df = pd.DataFrame(columns=['name', 'created_on'])

    for secret in secrets_list:
        df = df.append({'name': secret.name, 'created_on': secret.created_on}, ignore_index=True)

    return df

_config = config.read_config_file("variables_settings.yml")

akv_name = config.get_env_var("AKV_SERVICE_NAME", _config)
akv_uri = f"https://{akv_name}.vault.azure.net"

credential = DefaultAzureCredential()

df = retrieve_all_secrets_as_pandas(akv_uri, credential)

print(df.sort_values(by='created_on', ascending=False))