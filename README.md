# Nautical Mile — Learning Tracker

A small Flask app for tracking DevOps and GitOps learning milestones. Add learning goals and mark them as **To Learn** or **Completed**.

## Stack

- Python 3.11 and Flask
- SQLite
- Docker
- Kubernetes (Minikube)
- Argo CD for GitOps deployment
- GitHub Actions and Docker Hub for image builds

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## Build and run with Docker

```bash
docker build -t learning-tracker:local .
docker run --rm -p 5000:5000 learning-tracker:local
```

Then open [http://localhost:5000](http://localhost:5000).

## Deploy to Kubernetes

The manifests in [`k8s/`](./k8s/) create one app Pod and a `NodePort` Service on port `30080`. They deploy to the current namespace, which is `default` unless specified otherwise.

```bash
kubectl apply -f k8s/
kubectl get pods,services -n default
```

On a local Minikube installation, open the Service with:

```bash
minikube service learning-tracker-service -n default
```

### Access from GitHub Codespaces

Minikube's node IP (for example, `192.168.49.2`) is internal to the Codespace and is not directly reachable from your browser. Forward the Service port instead:

```bash
kubectl port-forward -n default svc/learning-tracker-service 8082:5000
```

Keep the command running. In VS Code's **Ports** tab, open port `8082` using its **Forwarded Address** and set the port protocol to **HTTP**. Use that address in your browser.

## Deploy with Argo CD

Argo CD watches this repository's `k8s/` directory, targets the `default` namespace, and has automated sync enabled in [`argocd-app.yaml`](./argocd-app.yaml).

Install Argo CD in the cluster once:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

If the GitHub repository is private, connect it in the Argo CD UI under **Settings → Repositories**. Use a GitHub token with read-only Contents access; do not commit the token to this repository.

Create or update the Argo CD Application:

```bash
kubectl apply -f argocd-app.yaml
```

To open the Argo CD UI from Codespaces:

```bash
kubectl port-forward -n argocd svc/argocd-server 8081:443
```

Keep the command running, then open port `8081` from the VS Code **Ports** tab using the **Forwarded Address**. Set its port protocol to **HTTPS**.

## Image builds

The GitHub Actions workflow in [`.github/workflows/ci.yaml`](./.github/workflows/ci.yaml) builds and pushes an image when code is pushed to `main`. It tags the image with the short commit SHA (for example, `sha-5e8667a`).

Configure the `skills` GitHub Actions environment with these secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` — a Docker Hub access token with permission to push images

After a new image is pushed, update the image tag in [`k8s/deployment.yaml`](./k8s/deployment.yaml) and push that manifest change. Argo CD follows the image tag in Git; it does not automatically select newly published Docker Hub tags.

## Data storage note

The app stores its SQLite database in `skills.db` inside its working directory. The current Kubernetes manifests do not configure persistent storage, so data may be lost when the Pod is replaced.
