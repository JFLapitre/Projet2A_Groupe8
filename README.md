# Prerequisite:  PDM 

Install PDM for your user with pip 

`> pip install --user pdm`

Check your PDM version with 

`> pdm --version`

Optionally, use uv "under the hood" for faster installation: 

`> pip install --user uv`

`> pdm config use_uv true`

## Note for Onyxia/k8s users

The installation can be handled by the setup script `init_project.sh`.

You can provide that configuration file as a custom initialization script for your vscode image. 

Be sure to provide the ports used by the app in the `Network access` configuration. For example, this app uses the `5000` port.

# How to install the app 

`> pdm install`

That's all 😊

# How to run the app 

```> pdm start```

This starts a server accessible on the link provided by onyxia.

The API is then documented on the endpoint /docs


To test the API with bruno you can click here.
[<img src="https://fetch.usebruno.com/button.svg" alt="Fetch in Bruno" style="width: 130px; height: 30px;" width="128" height="32">](https://fetch.usebruno.com?url=https%3A%2F%2Fgithub.com%2FJFLapitre%2FProjet2A_Groupe8.git "target=_blank rel=noopener noreferrer")