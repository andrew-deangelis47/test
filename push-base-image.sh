aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin  public.ecr.aws
docker build -t public.ecr.aws/f1i5f7i1/integrations_base -f Dockerfile-Integrations-Base .
docker push public.ecr.aws/f1i5f7i1/integrations_base