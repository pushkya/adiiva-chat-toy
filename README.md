1. Install Docker: https://www.docker.com/products/docker-desktop/
2. Install anaconda: https://www.anaconda.com/download/success
3. Open pycharm and create conda env adiiva-ai: conda create --name adiiva-ai
4. Create a folder adiiva and pull the project in your project directory using: git clone git@github.com:pushkya/adiiva-chat-toy.git
5. Before running the project make sure you have Huggingface API key. If you dont have one create a new key here: https://huggingface.co/settings/tokens
6. Once you get the API key build your docker using: cd adiiva-chat-toy & docker build -t adiiva-chat-toy .
7. Once the build is complete run the container: docker run --env HF_API_TOKEN=YOUR_API_KEY --env LLM_PROVIDER=huggingface -p 8000:8000 adiiva-chat-toy
   

