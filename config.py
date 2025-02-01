import boto3
from botocore.config import Config

# Configuration de Boto3
my_config = Config(
    region_name='us-west-2',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Initialisation du client Redshift Data
client = boto3.client('redshift-data', config=my_config)

# Paramètres de connexion
database = 'dev'
workgroup_name = 'wz-solutions-redshift-workgroup'
db_user = 'admin'

# Fonction pour exécuter une requête SQL
def execute_query(sql_query):
    try:
        response = client.execute_statement(
            Database=database,
            WorkgroupName=workgroup_name,
            Sql=sql_query
        )
        return response
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

# Initialisation du client Bedrock pour l'agent AI
bedrock_client = boto3.client('bedrock', config=my_config)

# Paramètres de l'agent AI
agent_id = 'PJFOYVVMNI'
agent_arn = 'arn:aws:bedrock:us-west-2:767828765654:agent/PJFOYVVMNI'
role_arn = 'arn:aws:iam::767828765654:role/service-role/AmazonBedrockExecutionRoleForAgents_4U6SYV6XA7R'

# Fonction pour invoquer l'agent AI
def invoke_agent(prompt):
    try:
        response = bedrock_client.invoke_agent(
            agentId=agent_id,
            agentArn=agent_arn,
            roleArn=role_arn,
            prompt=prompt
        )
        return response
    except Exception as e:
        print(f"Erreur lors de l'invocation de l'agent : {e}")
        return None
