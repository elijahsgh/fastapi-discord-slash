podman build . -t gcr.io/tamarintech-sites/fastapi-discord:latest
DIGEST=$(podman images --format '{{.Digest}}'  gcr.io/tamarintech-sites/fastapi-discord:latest)
podman push gcr.io/tamarintech-sites/fastapi-discord:latest --remove-signatures --format docker
echo $DIGEST

gcloud run deploy testdiscordintention \
--image=gcr.io/tamarintech-sites/fastapi-discord:latest \
--platform=managed \
--region=us-central1 \
--project=tamarintech-sites