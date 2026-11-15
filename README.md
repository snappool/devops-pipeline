# DevOps Pipeline Project

A small Flask app with a complete delivery pipeline around it:
**code -> test -> containerize -> publish**, automatically on every `git push`.

```
git push  ->  GitHub Actions  ->  lint + tests  ->  build Docker image  ->  push to ghcr.io
```

## Project layout

| File | What it does |
|------|--------------|
| `app.py` | The Flask app (`/`, `/health`, `/greet`) |
| `tests/test_app.py` | pytest tests |
| `Dockerfile` | Recipe for building the container image |
| `docker-compose.yml` | Runs the container with one command |
| `.github/workflows/ci.yml` | The CI pipeline |

## Part 1: Run it without Docker first

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python app.py                   # open http://localhost:5000
pytest -v                       # run tests
flake8 . --max-line-length=100 --exclude=venv   # lint
```

## Part 2: Docker basics (learn by doing)

**Concepts**
- **Image**: a read-only package containing your app + everything it needs (Python, libraries).
- **Container**: a running instance of an image. Think "image = class, container = object".
- **Dockerfile**: the recipe that builds an image, one instruction per layer.
- **Registry**: a place to store images (Docker Hub, GitHub's ghcr.io).

**Try these in order**

```bash
docker build -t myapp .                  # build an image from the Dockerfile
docker images                            # see it listed
docker run -p 5000:5000 myapp            # run it; open http://localhost:5000
docker run -d -p 5000:5000 --name web myapp   # -d = run in background
docker ps                                # list running containers
docker logs web                          # see the app's output
docker exec -it web sh                   # open a shell inside the container
docker stop web && docker rm web         # stop and remove it
```

**Then use compose** (the same thing, but one command):

```bash
docker compose up --build       # start
docker compose down             # stop and clean up
```

**Experiments to understand it**
1. Change the message in `app.py`, rebuild, and watch which layers are cached.
2. Run `docker exec -it web whoami`. It prints `appuser`, not `root`. Why is that good?
3. Compare image sizes: change `python:3.12-slim` to `python:3.12` and rebuild.

## Part 3: The CI pipeline

1. Create a new empty repo on GitHub (for example `devops-pipeline`).
2. Push this folder to it:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/devops-pipeline.git
   git push -u origin main
   ```
3. Open the **Actions** tab on GitHub. You should see the `CI` workflow run: lint, tests, then image build and push.
4. Your image appears under your profile -> **Packages**.
5. Break a test on purpose, push, and watch the pipeline go red. Fix it and watch it go green.

Add a status badge to the top of this README:
`![CI](https://github.com/<your-username>/devops-pipeline/actions/workflows/ci.yml/badge.svg)`

## Next phases

- [ ] Add Postgres to `docker-compose.yml` and store data from the app
- [ ] Kubernetes manifests (Deployment, Service, ConfigMap) on kind or minikube
- [ ] Automatic deploy step after the image is pushed
- [ ] `/metrics` endpoint + Prometheus + Grafana dashboard and alert
- [ ] Terraform or Ansible for infrastructure
