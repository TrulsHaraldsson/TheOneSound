# TheOneSound
The One Sound is an application that tries to mix the best parts from the famous music provider Spotify with the free encyclopedia Wikipedia. More precisely, the application should be a library containing information about bands, albums and
tracks that users provide, while also allowing users to listen to music. Moreover should the application work as a social media were users can interact with each other and let each user have their own profile-page.

## Installation Instructions
To get started is easy since the server is hosted on google app engine. You need to be listed as an editor to access The One Sound on google app engine. Here is a step by step instruction to get going. 
-1 The first thing you need to do is check that python is installed. Do this by typing "python -V" in the terminal (it should be python 2.7).
-2 Then you need to install the google cloud SDK.
  * Start by downloading the google cloud SDK, it is found at this link https://cloud.google.com/appengine/docs/python/quickstart 
  * Click the "Download the sdk" button. You will then be redirected to a guide how to download, install and initialize the sdk. Follow it.
  * When prompted to choose wich project to be set as current, choose The One Sound.
    
-3 When the google cloud sdk is up and running you need to clone The One Sound from github. Type "git clone [URL]" in the terminal where you want to save it.
-4 Once dowloaded, a local server can be started to test that everything is working. Go into the folder where the app.yaml file is and write in the terminal "dev\_appserver.py app.yaml". This should start a local server on port 8080. Check that it works. P.S. you may be prompted to download extra components for it to work.
-5 To later on deploy the application to app engine, you need to be listed as editor. You can check your projects by typing "gcloud projects list" in the terminal. To deploy, you should be in the folder of the app.yaml file and type "gcloud app deploy app.yaml index.yaml" in the terminal. This may take some time.
-6 Check that it is working by typing "gcloud app browse", or write the url in your browser.

Congratulations, you are done!
