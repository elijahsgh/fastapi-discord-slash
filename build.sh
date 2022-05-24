podman build . -t gcr.io/tamarintech-sites/fastapi-discord:latest
DIGEST=$(podman images --format '{{.Digest}}'  gcr.io/tamarintech-sites/fastapi-discord:latest)
podman push gcr.io/tamarintech-sites/fastapi-discord:latest --remove-signatures --format docker
echo $DIGEST

