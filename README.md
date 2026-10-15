# Flask Currency Converter: CI/CD Pipeline on AWS EC2

A small Flask app that converts between GBP, USD and CAD using live exchange rates. The app itself is simple on purpose. The point of this project is how it gets built, packaged and deployed.

The app runs in Docker containers behind an Nginx reverse proxy on an AWS EC2 instance. Jenkins redeploys it when I push changes to this repo.

## How it fits together

```
Browser --> Nginx (port 80) --> Flask app container (port 5000) --> exchange rate API
```

Deployment flow:

```
git push --> Jenkins --> docker compose build and up --> EC2
```

## Tech stack

- Python 3.11 and Flask
- Docker and Docker Compose
- Nginx as a reverse proxy
- Jenkins for CI/CD
- AWS EC2 for hosting
- Bash for server setup

## What's in this repo

| File | What it does |
| --- | --- |
| `app.py` | The Flask app. Takes an amount and two currencies, checks the input, fetches live rates and shows the result. |
| `external.txt` | Python dependencies, installed during the image build. |
| `Dockerfile` | Builds the Flask image from `python:3.11-slim`. |
| `docker-compose.yml` | Runs two containers: `flask-app` (port 5000, internal only) and `nginx-proxy` (port 80, public). |
| `nginx/nginx.conf` | Nginx config that forwards requests to the Flask container. |

## The app

- Supports GBP, USD and CAD.
- Rejects negative amounts and unsupported currencies with a clear error message.
- Pulls live rates from the free ExchangeRate-API endpoint.
- Shows an error message if the rates can't be fetched.

## Run it locally

You need Docker and Docker Compose installed.

```bash
git clone https://github.com/praise-oguns/flask-cicd-aws-pipeline.git
cd flask-cicd-aws-pipeline
docker compose up --build
```

Then open http://localhost in your browser. Nginx listens on port 80 and passes traffic to Flask.

## Deploy on AWS EC2

1. Launch an EC2 instance (Ubuntu).
2. In the security group, allow port 80 from anywhere and port 22 from your own IP only.
3. Install Docker and Docker Compose on the instance.
4. Clone this repo and run `docker compose up -d --build`.
5. Visit the instance's public IP in a browser.

## CI/CD with Jenkins

When I push to `main`, Jenkins [webhook or polling: confirm which] pulls the latest code, rebuilds the images and restarts the containers on the EC2 instance, so I never deploy by hand.

Pipeline steps:

1. Check out the latest code from GitHub
2. Build the images with Docker Compose
3. Restart the containers on the server

Jenkins runs on [where Jenkins runs: confirm].

## What I would improve next

- Run the app with Gunicorn instead of Flask's built-in development server.
- Add the Jenkinsfile to this repo so the pipeline is version controlled.
- Add HTTPS with a certificate on the Nginx container.
- Add basic tests and run them in the pipeline before deploying.
- Add a request timeout and error handling around the exchange rate call.

## Author

Praise Oguns
GitHub: [praise-oguns](https://github.com/praise-oguns)
LinkedIn: [praise-oguns-17a082240](https://www.linkedin.com/in/praise-oguns-17a082240)
