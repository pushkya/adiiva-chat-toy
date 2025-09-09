1. Install Docker: https://www.docker.com/products/docker-desktop/
2. Install anaconda: https://www.anaconda.com/download/success
3. Open pycharm create a new project PROJECT_NAME, select CUSTOM ENVIRONMENT and select environment type as Conda. Select Python version as 3.9
4. Once project is created open terminal in Pycharm and create conda env adiiva-ai: *conda create --name adiiva-ai*
5. Then activate your environment: *conda activate adiiva-ai*
6.  If you dont have the ssh-key open terminal and type *ssh-keygen* and press enter, for passphrase press enter. Once the key is created, open the file where public key is created by the extension *.pub*
7. Then go to github->settings->SSH and GPG keys->New SSH key. Give title to your key and paste the public key in *Key*. Click Add SSH key
8. Create a folder adiiva and pull the project in your project directory using: *git clone git@github.com:pushkya/adiiva-chat-toy.git*
9. Before running the project make sure you have Huggingface API key. If you dont have one create a new key here with *Write* permission: https://huggingface.co/settings/tokens (Create new account if you dont have). Save the API key in a notepad.
10. Open docker desktop to start your docker engine.  
11. Once you get the API key build your docker using: *cd adiiva-chat-toy* , *docker build -t adiiva-chat-toy .*
12. If you face DNS issues, open Control Panel->Network and Sharing->Change adapter settings->Internet Protocol Version 4. Click on it and hit Properties. Add Prefered DNS as 8.8.8.8 and Alternate DNS as 1.1.1.1. Once added run the build command again
13. Once the build is complete run the container: *docker run --env HF_API_TOKEN=YOUR_API_KEY --env LLM_PROVIDER=huggingface -p 8000:8000 adiiva-chat-toy*
   

