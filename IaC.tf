provider "aws" {
  region = "us-west-2" #region Oregan
}

# --- S3 BUCKET (Stockage des fichiers CSV) ---
resource "aws_s3_bucket" "data_bucket" {
  bucket = "veolia-data-quality-bucket"
}

# --- REDSHIFT CLUSTER (Base de données analytique) ---
resource "aws_redshift_cluster" "redshift_db" {
  cluster_identifier   = "veolia-redshift-cluster"
  database_name        = "veolia_db"
  master_username      = "admin"
  master_password      = "SuperSecurePass123"
  node_type            = "dc2.large"
  cluster_type         = "single-node"
  publicly_accessible  = true
}

# --- INSTANCE EC2 (Exécution de l'agent IA) ---
resource "aws_instance" "agent_ec2" {
  ami           = "ami-12345678"  # Mettre une AMI Amazon Linux 2 valide
  instance_type = "t2.medium"

  tags = {
    Name = "AgentIA"
  }
}

# --- IAM ROLE (Permissions pour accéder à Bedrock et Redshift) ---
resource "aws_iam_role" "bedrock_role" {
  name = "bedrock-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "bedrock.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy_attachment" "attach_redshift_s3" {
  name       = "redshift-s3-access"
  roles      = [aws_iam_role.bedrock_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# --- AMAZON BEDROCK (IA Générative) ---
resource "aws_bedrock_model" "mistral_ai" {
  model_id = "mistral.mixtral-8x7b-instruct-v0:1"
}