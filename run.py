import os
import subprocess
import sys


CONTAINER_NAME = "tg-audio2text"
SESSION_FILE = "TgAudio2Text.session"
SESSION_FILE_PATH = os.path.abspath(SESSION_FILE)
SESSION_FILE_PATH_CONTAINER = f"/app/{SESSION_FILE}"
DOCKERFILE_DIR = os.path.dirname(__file__)
ENV_FILE = os.path.join(DOCKERFILE_DIR, ".env")

def run(command):
    print(f"→ {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    print("🔁 Rebuilding Docker container...")

    # Stop and remove old container (ignore errors)
    run(f"docker stop {CONTAINER_NAME} || true")
    run(f"docker rm {CONTAINER_NAME} || true")

    # Build new image
    run(f"docker build -t {CONTAINER_NAME} {DOCKERFILE_DIR}")

    # Run container
    run(f'docker run -d \
        --name {CONTAINER_NAME} \
        --env-file .env \
        -v "{SESSION_FILE_PATH}:{SESSION_FILE_PATH_CONTAINER}" \
        {CONTAINER_NAME}')
    
    # Remove previous images
    run(f"docker image prune -f")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        print("❌ Error running one of the commands.")
        sys.exit(1)
