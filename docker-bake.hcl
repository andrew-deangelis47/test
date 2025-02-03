// TODO variable validation when bake 0.19 is out
// https://github.com/docker/buildx/pull/2794

BUILD_ANNOTATIONS = []

variable "REGISTRY" {
  default = "431105233043.dkr.ecr.us-east-1.amazonaws.com"
}

variable "BUILD_ID" {
}

variable "DEPLOY" {
  default = "false"
}

group "default" {
  targets = [
    "base"
  ]
}

group "customers" {
  targets = [
    "example_customer",
    "gsmw-auto-quote"
  ]
}

target "base" {
  target = "base"
  dockerfile = "Dockerfile.cicd"
  tags = [
    BUILD_ID != "" ? "${REGISTRY}/integrations/base:${BUILD_ID}" : "",
    BUILD_ID == "" ? "integrations/base:development" : "",
    DEPLOY == "true" ? "${REGISTRY}/integrations/base:latest" : "",
  ]
  cache-from = ["type=registry,ref=${REGISTRY}/integrations/base:latest"]
  annotations = BUILD_ANNOTATIONS
  platforms = [
    "linux/amd64"
  ]
}


target "customer-gsmw-auto-quote" {
  contexts = {
    base = "target:base"
  }
  dockerfile = "Dockerfile.cicd"
  target = "customer"
  args = {
    CUSTOMER = "gsmw-auto-quote",
    ERP_SYSTEM = "hubspot",
    PURPOSE = BUILD_ID != "" ? "release" : "development",
    HTTP_PORT = "1025"
  }
  tags = [
    BUILD_ID != "" ? "${REGISTRY}/integrations/customers/gsmw-auto-quote:${BUILD_ID}" : "",
    BUILD_ID == "" ? "integrations/customers/gsmw-auto-quote:development" : "",
    DEPLOY == "true" ? "${REGISTRY}/integrations/customers/gsmw-auto-quote:release" : "",
  ]
  annotations = BUILD_ANNOTATIONS
  platforms = [
    "linux/amd64"
  ]
}
