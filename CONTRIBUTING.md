# Contributing

### How to run the Dockerfile locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-flask-api sh -c "flask run"
```
**Command information:**
- `-d` run the in the background
- `-p` run on the port `5000`
- `-w` sets the working directory inside the container (`/app`)
- `-v` mounts the storage volume to the container
- `rest-flask-api` name of the container
- `sh -c "flask run"` shell executable command that runs the flask development server
