Flask Currency Converter on AWS with Jenkins and Terraform

I built this to practise getting code from my laptop to a server without anyone logging in by hand. The app is a small currency converter. The setup around it is the interesting part.

I originally built this pipeline manually in an AWS Learner Lab, then refactored the whole setup into Terraform on my own AWS account so I wouldn't lose the architecture when the lab expired. Now, when I push a change to GitHub, Jenkins picks it up and redeploys the app automatically.

Terraform provisions the AWS infrastructure, so the whole environment can be created or deleted with a few commands instead of setting everything up manually.

Table of Contents
What the App Does
How It Works
AWS Infrastructure
Project Screenshots
Project Structure
Run It on Your Own Machine
Build the Whole Thing on AWS
What I Learned
What's Next
Author
What the App Does
Converts between GBP, USD and CAD using live exchange rates.
Rejects negative amounts and unsupported currencies with a clear message.
Shows an error if the exchange rate service can't be reached.
How It Works

The idea is simple: I push code to GitHub, Jenkins detects the change, and the app gets updated on the server without me having to log in and deploy it manually.

text
I push to GitHub
      |
      v
Jenkins (its own EC2 instance)
checks the repo every 2 minutes
      |
      v
Jenkins connects to the app server over SSH
using its private IP inside the VPC
      |
      v
The app server pulls the code
and rebuilds the containers
      |
      v
Browser --> Nginx (port 80)
                 |
                 v
          Flask container (port 5000)


The app runs in Docker Compose with two containers. Nginx is the only container exposed to the internet. Flask is only reachable through Nginx.

AWS Infrastructure

Terraform provisions the AWS infrastructure, including:

A custom VPC with one public subnet, an internet gateway and a route table.
Two Ubuntu 24.04 EC2 instances: one for Jenkins and one for the app.
Security groups controlling SSH, Jenkins web access and public HTTP access.
An IAM role and instance profile on the app server for AWS Systems Manager (SSM) access.
An AWS key pair for SSH access.
Encrypted EBS volumes and IMDSv2 enforcement on both instances.
Security Configuration
SSH and the Jenkins web interface on port 8080 are restricted to my IP address.
The app server only accepts SSH connections from the Jenkins security group.
The app is accessible over HTTP on port 80.
Flask runs behind Nginx and is not directly exposed to the internet.
Both EC2 instances require IMDSv2 and use encrypted disks.
Docker and Git are installed automatically on both servers using user_data startup scripts.

Jenkins runs as a Docker container on its own EC2 instance. The app server pulls the latest code from GitHub and rebuilds the containers when Jenkins triggers a deployment.

Project Screenshots

The screenshots show the infrastructure being provisioned, the pipeline running, the live app updating after a code change, and the infrastructure being destroyed.

1. Terraform Infrastructure Provisioning and Outputs

Shows Terraform creating the AWS infrastructure and printing the outputs needed to access Jenkins and the app.

<!-- Add your Terraform apply and output screenshots here. -->

2. Automated CI/CD Pipeline

Shows the Jenkins Stage View during a deployment.

<!-- Add your Jenkins Stage View screenshot here. -->

3. Live App: Before and After a Code Push

Shows the app before a change and after Jenkins deploys the updated code.

<!-- Add your before-and-after screenshots here. -->

4. Tearing Down the Environment

Shows Terraform destroying the infrastructure when the environment is no longer needed.

<!-- Add your terraform destroy screenshot here. -->

Project Structure
text
flask-cicd-aws-pipeline/
├── app.py
├── external.txt
├── Dockerfile
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── Jenkinsfile
├── terraform/
│   └── Infrastructure as Code
└── screenshots/
    └── Project screenshots

Run It on Your Own Machine

You need Docker and Docker Compose installed.

Clone the repository:

bash
git clone https://github.com/praise-oguns/flask-cicd-aws-pipeline.git
cd flask-cicd-aws-pipeline


Build and start the containers:

bash
docker compose up --build


Open the app in your browser:

http://localhost

To stop the containers, press Ctrl+C and run:

bash
docker compose down

Build the Whole Thing on AWS

You need:

An AWS account with permissions to create the required resources.
Terraform installed.
The AWS CLI configured with your credentials.
An SSH key pair, with access to the matching private key.
A GitHub account and access to the project repository.
1. Configure Terraform

Create terraform/terraform.tfvars with your details:

hcl
my_ip           = "YOUR.IP.ADDRESS/32"
public_key_path = "C:/Users/you/.ssh/id_ed25519.pub"


Replace the example IP address with your own public IP address and update the key path for your machine.

Keep terraform.tfvars and private keys out of version control.

2. Build the Infrastructure

From the project root, run:

bash
cd terraform
terraform init
terraform plan
terraform apply


Review the plan and confirm the changes when prompted.

Terraform provisions the AWS infrastructure and prints outputs, including the Jenkins URL, app URL and app server private IP.

3. Set Up Jenkins

Wait about 3 minutes for the startup scripts to finish, then open the jenkins_url printed by Terraform.

Unlock Jenkins by retrieving the initial administrator password from the Jenkins container:

bash
sudo docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword


Install the suggested plugins and the SSH Agent plugin.

4. Configure SSH Credentials

In Jenkins, add an SSH credential with these details:

ID: app-server-key
Username: ubuntu
Private key: The private key matching the public key supplied to Terraform.

The Jenkins credential ID must match the one referenced in the Jenkinsfile.

5. Configure the Deployment Pipeline

Put the app_private_ip value printed by Terraform into the Jenkinsfile and push the change to GitHub.

Create a Pipeline job in Jenkins with the following configuration:

Repository: https://github.com/praise-oguns/flask-cicd-aws-pipeline.git
Branch: */main
Script path: Jenkinsfile
Build trigger: Poll SCM
Schedule: H/2 * * * *

This tells Jenkins to check the repository approximately every two minutes. It does not require a GitHub webhook.

6. Test the Deployment

Push a change to app.py and watch Jenkins pick it up and deploy it.

Once the pipeline completes, open the app_url printed by Terraform to see the updated app.

The goal is to go from a code change on GitHub to a live update without manually logging in to the app server.

7. Tear Down the Infrastructure

When you're done experimenting, run:

bash
cd terraform
terraform destroy


Review the resources Terraform plans to remove and confirm the destruction.

This removes the infrastructure managed by this Terraform configuration. Make sure you have saved anything you want to keep before destroying it.

Remember that AWS charges can still apply while the infrastructure is running, so don't leave the servers running when you're finished.

What I Learned
The app server only accepts SSH from the Jenkins security group, and that rule is based on the source security group rather than a public IP. Jenkins has to connect to the private IP (10.0.1.x), not the public one.
Moving the setup from an AWS Learner Lab into Terraform means I own the code for the whole network and can delete everything and rebuild it in a few minutes without paying for idle EC2 time.
Polling every two minutes (H/2 * * * *) lets me keep the Jenkins page restricted to my IP. A GitHub webhook would require inbound access from GitHub's webhook delivery infrastructure, which would mean changing the current access rules.
Docker Compose makes it straightforward to run Flask behind Nginx without exposing the Flask container directly to the internet.
Terraform makes the infrastructure repeatable, while Jenkins handles the application deployment.
What's Next
Add unit tests and run them in the pipeline before deployment.
Add a domain name and HTTPS using Let's Encrypt with Nginx.
Author

Praise Oguns

GitHub:github.com/praise-oguns
LinkedIn: www.linkedin.com/in/praise-oguns
