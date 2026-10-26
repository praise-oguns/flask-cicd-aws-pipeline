# Flask Currency Converter on AWS with Jenkins and Terraform

I built this to practise getting code from my laptop to a server without anyone logging in by hand. The app is a small currency converter. The setup around it is the interesting part.

When I push a change to GitHub, Jenkins picks it up and redeploys the app. Terraform builds all the servers, so the whole environment can be created or deleted with one command.

## What the app does

- Converts between GBP, USD and CAD using live exchange rates.
- Rejects negative amounts and unsupported currencies with a clear message.
- Shows an error if the exchange rate service can't be reached.

## How it works

```
I push to GitHub
      |
Jenkins (its own EC2 instance) checks the repo every 2 minutes
      |
Jenkins connects to the app server over SSH
      |
The app server pulls the code and rebuilds the containers
      |
Browser --> Nginx (port 80) --> Flask container (port 5000)
```

The app runs in Docker Compose with two containers. Nginx is the only one open to the internet. Flask is only reachable through Nginx.

## What Terraform builds

- A VPC with one public subnet, an internet gateway and a route table
- Two Ubuntu 24.04 EC2 instances: one for Jenkins, one for the app
- Security groups: SSH and the Jenkins web page are only open to my IP, the app server accepts SSH from Jenkins, and port 80 is open to everyone
- An IAM role on the app server that only allows AWS Systems Manager access
- Encrypted disks, and IMDSv2 required on both instances

Jenkins runs as a Docker container on its own server. Docker and Git are installed on both servers by a startup script.

## Files

```
app.py                 The Flask app
external.txt           Python dependencies
Dockerfile             Builds the Flask image
docker-compose.yml     Runs Flask and Nginx
nginx/nginx.conf       Nginx reverse proxy config
Jenkinsfile            The deploy pipeline
terraform/             Infrastructure code
```

## Run it on your own machine

You need Docker and Docker Compose.

```bash
git clone https://github.com/praise-oguns/flask-cicd-aws-pipeline.git
cd flask-cicd-aws-pipeline
docker compose up --build
```

Open http://localhost in your browser.

## Build the whole thing on AWS

You need Terraform, the AWS CLI set up with your credentials, and an SSH key.

1. Create `terraform/terraform.tfvars` with your details:
   ```
   my_ip = "YOUR.IP.ADDRESS/32"
   public_key_path = "C:/Users/you/.ssh/id_ed25519.pub"
   ```
2. Build the servers:
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```
3. Open the `jenkins_url` that Terraform prints. Unlock Jenkins with the password from `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`, install the suggested plugins and the SSH Agent plugin.
4. Add an SSH credential with the ID `app-server-key` and the username `ubuntu`, using the private key that matches your public key.
5. Put the `app_private_ip` from Terraform into the `Jenkinsfile`.
6. Create a Pipeline job from this repo, and tick Poll SCM with `H/2 * * * *`.
7. Push a change to `app.py` and watch Jenkins deploy it. The app is at the `app_url` that Terraform prints.

When you're done, run `terraform destroy` so you don't pay for idle servers.

## What I learned

- The app server only accepts SSH from the Jenkins security group, and that rule only matches private addresses. Jenkins has to connect to the private IP, not the public one.
- Keeping infrastructure in code means I can delete everything and rebuild it in a few minutes.
- Polling every 2 minutes lets me keep the Jenkins page locked to my IP. A GitHub webhook would need that port open to the internet.

## Next

- Add tests and run them in the pipeline before it deploys.
- Add HTTPS to Nginx.

## Author

Praise Oguns
GitHub: [praise-oguns](https://github.com/praise-oguns)
LinkedIn: [praise-oguns-17a082240](https://www.linkedin.com/in/praise-oguns-17a082240)