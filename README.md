# setting up your workspace

## Installation requirements
### Azure Account
if you don't have an Azure Acount you can sign up for a free trial Account.

### necessary software
[python 3.7.5 64-bit](https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe)  
When installing Python, make sure to choose the version specified above, Python 3.7.5 in 64-bit version. Also install Pip with Python and tick add Python to Environment Variables during your installation.  
[vs code](https://code.visualstudio.com/download#)  
[docker for windows](https://docs.docker.com/docker-for-windows/install/)  
when installing docker for windows do not mark the option use Windows Container instead of Linux Container  
Also note that you have to create a docker account in order to install the software  
[azure cli](https://docs.microsoft.com/de-de/cli/azure/install-azure-cli-windows?view=azure-cli-latest)

### optional software
[git client](https://git-scm.com/download/win)  

### recommended vs code extensions
for installing the extensions, you can either click the links below and click 
on install, or you can open VS Code go to marketplace and type in the extensions there

[python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)  
[code runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner)  
[intelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)  
[docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)  
[Azure App Service](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice)  
When installing extensions and loading the workspace, vs code will prompt for further installs. Always click allow and install.


## set-up instructions
### how to use git
```bash
git echo "# geekweekend" >> README.md  
git init  
git add README.md  
git commit -m "first commit"   
git remote add origin https://github.com/csam1850/geekweekend.git  
git push -u origin master  
```

### setting up your python-workspace
Please note I deliberatly uploaded .vscode to github which contains hardcoded 
information from my personal workspace, which you need to adjust.
To do that you have to open the folder .vscode, right click workscpace.code-workspace and open it with an editor. 
The important part is the PythonPath environment variable, which you have to adjust, so it points to your repository. 
If you encounter a Module-not-found error lateron you probably have an issue with your PythonPath.  
To set up your workspace go to vs code / File / open workspace and select the workspace file in the .vscode folder.
  

```shell
# this command creates a virtual environment  
python -m venv venv  
# activating the environment  
venv\Scripts\activate  
# installing the libraries with the specified version  
pip install -r requirements.txt
```

# starting the application
### starting local Flask-Server 

```shell
set FLASK_APP=app.py
flask run
```
  
### starting the docker container 
take care that the port is not blocked by the flask application

```shell
docker build -t geekweekendcontainer.azurecr.io/classifier:latest .
docker run -d -p 5000:5000 geekweekendcontainer.azurecr.io/classifier:latest
```

### Creating a Docker Container and pushing it to a registry
pushing the container image to azure docker registry  
go to Azure portal first and create a container registry - make sure to put
admin on enabled and the name of the container registry should fit to the first part of the tag of the image. In our case this is geekweekendcontainer  

```shell
# login to azure
az login
# login to azure container registry
az acr login --name <acrName>
```  
right click the image and push *OR ALERNATIVELY* on the Command Palette (Ctrl+Shift+P), select Docker: Push.

If the notification pops up that further authentification is required, try the following:  
```shell
az acr credential show --name <azure-container-registry-name>  
docker login <azure-container-registry-name>.azurecr.io --username <registry-username>  
```

### Deploying a container image to Azure App Service
right click the image in the registry and press `Deploy Image to Azure App Service`  
follow the prompts  
go to Azure App Service in vs code right click your application and press
`Add New Setting...`. 
Type in WEBSITES_PORT and 5000 to expose the port of your container

# Workshop Challenge
Go to https://www.customvision.ai/ and create a workspace. Generate an image classifier from the test images contained in the directory. Export the model and replace the existing model in the application with this one.  
You can use the tutorials mentioned in the links below

# Sources
## dataset
https://www.kaggle.com/moltean/fruits

## example models from kaggle
https://www.kaggle.com/mitch9090/fruit-dataset-image-classification-network  
https://www.kaggle.com/litzar/fruits-classification  
https://www.kaggle.com/aninditapani/cnn-from-scratch-with-98-accuracy  
https://www.kaggle.com/waltermaffy/fruit-classification-pca-svm-knn-decision-tree 

## example Flask-apps
https://github.com/OkanKY/keras-flask-webapp  
https://github.com/ibrahimokdadov/upload_file_python

## data augmentation
https://gogul.dev/software/image-classification-python  
https://kapernikov.com/tutorial-image-classification-with-scikit-learn/  
https://rpubs.com/Sharon_1684/454441  

## support vector machines
https://jakevdp.github.io/PythonDataScienceHandbook/05.07-support-vector-machines.html  
  
# Tutorials
## creating docker images
https://code.visualstudio.com/docs/python/tutorial-create-containers  
https://code.visualstudio.com/docs/azure/docker  
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers  

## deploying docker image
https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-custom-docker-image  
https://docs.microsoft.com/en-us/azure/python/tutorial-deploy-containers-01  

## using azure custom vision
https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier  
https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-your-model  
https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-model-python  
