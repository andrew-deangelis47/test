# Print statement wording is important as the Jenkins job is checking for text matches such as 'Tests are OK'

# Import standard libraries
import os
import datetime
from glob import glob

# Build image
image_name = "431105233043.dkr.ecr.us-west-2.amazonaws.com/integrations_test:latest"
os.system("touch config.yaml")
os.system("mkdir logs")
os.system("mkdir custom_processors")
print("\n\n\n\n\n")
print("=======================")
print("Building Docker test image")
os.system(f"docker build -t {image_name} -f integrations/Dockerfile . --build-arg rm_config=True")

# Get current time
timestamp = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
test_run = f"integrations-test-{timestamp}"

# If this script is running in Docker, that means it is on Jenkins
if os.path.exists("/.dockerenv"):
    home_dir = "/home/ubuntu/jenkins_data/userContent"
else:
    home_dir = "/var/jenkins_home/userContent"


print("\n\n\n\n\n")
print("=======================")
print("Running Docker tests")
# Run 4 commands together in each docker container. We must both run the tests and move the coverage files
# Store the result of the first, the test run, and return it as an exit code so we can check if all tests passed
docker_command = f"docker run -e ERP_VERSION=default -v {home_dir}:/var/user_content -v /var/jenkins_home/integrations/secrets.ini:/home/custom_integration/secrets.ini {image_name} /bin/bash -c 'pytest --cov-fail-under=90 --cov-config=integrations/.coveragerc --cov-report=html"
cp_command = f"; ex_code=$?; mv coverage_html_report /var/user_content/{test_run}"

# Get all the directories inside of "integrations"
dirs = glob("integrations/*/")
passed = True

# Run baseintegration and all other ERP tests
for dir in dirs:
    coverage_dir_label = dir.rsplit('/', 1)[0].split("/")[1]

    # adding Plex_V2 in here because we need to get this merged. Unit test coverage is WIP in another branch ("plex_v2_unit_tests").
    # several customer are already live for Plex_V2 so we can feel safe about merging in
    if any(substring in dir for substring in ["__pycache__", "venv", "googlesheets", "sage", "plex_v2", "jobscope", "dynamics", "customers", "jenkins", "m2m_api"]):
        continue
    elif "e2" in dir and "e2_cloud" not in dir:
        # e2 is a special case because we have two versions we need to run tests for. e2 cloud is not special tho
        e2_default_result = os.system(f"{docker_command} --cov={dir} integrations/e2/tests/test_e2_default.py {cp_command}-{coverage_dir_label}; exit $ex_code'")
        shop_system_command = docker_command.replace("ERP_VERSION=default", "ERP_VERSION=e2_shop_system")
        # do not run coverage for e2 shop system as it will not pass
        e2_shop_system_result = os.system(f"{shop_system_command} integrations/e2/tests/test_e2_shop_system.py {cp_command}-{coverage_dir_label}; exit $ex_code'")
        result = e2_shop_system_result + e2_default_result
    elif "m2m" in dir or "globalshop" in dir or "baseintegration" in dir or "mietrak_pro" in dir or "jobboss" in dir:
        # we do not run coverage for epicor or cetec yet -- this should be removed later
        result = os.system(f"{docker_command} {dir} {cp_command}-{coverage_dir_label}; exit $ex_code'")
    else:
        result = os.system(f"{docker_command} --cov={dir} {dir} {cp_command}-{coverage_dir_label}; exit $ex_code'")
    if result != 0:
        passed = False

print("\n\n\n\n\n")
print("=======================")
print("Tests complete")
# Check if all tests passed
if passed:
    print("Tests are OK")
else:
    print("Tests failed")
    print("Check failed")

print("\n\n\n\n\n")
print("=======================")
# Create zip file of all coverage reports and serve to userContent in Jenkins so it's accessible via browser
print("Creating zip file of coverage files to serve to Bitbucket")
os.chdir("/var/jenkins_home/userContent")
os.system(f"tar -zcvf {test_run}.zip {test_run}-*")
print("Deleting excess directories which are not zipped")
os.system(f"rm -rf {test_run}-*")
print(f"Coverage report: https://jenkins.paperlessparts.com/userContent/{test_run}.zip")

print("\n\n\n\n\n")
print("=======================")
print("Running safety")
# run safety check
result = os.system(f"docker run {image_name} safety check --policy-file=integrations/.safety-policy.yml")
if result == 0:
    print("Safety check is OK")
else:
    print("Safety check failed")
    print("Check failed")

print("\n\n\n\n\n")
print("=======================")
print("Running flake")
# run flake check
result = os.system(f"docker run {image_name} flake8 --config=integrations/.flake8.ini")
if result == 0:
    print("Flake is OK")
else:
    print("Flake failed")
    print("Check failed")
