# Buildpack python-ffmpeg

Create customer Python buildpack with `ffpmep` binary installed.

## Requirement

* [Pack](https://github.com/buildpacks/pack)
* [Docker](https://www.docker.com/products/docker-desktop/)

## Build buildpack

* Create `run` and `build` base image:

```bash
~$ for i in build run; do docker build -t "diablo02000/buildpack-base-${i}:python3-ffmpeg" --target "${i}" --push . ;done
```

The command below will build the Docker base image and push to Dockerhub. 

* Create buildpack:

```bash
~$ pack builder create diablo02000/buildpack:python3-ffmpeg  --config builder.toml && docker push diablo02000/buildpack:python3-ffmpeg
```

The command below build the buildpack and push on Dockerhub
