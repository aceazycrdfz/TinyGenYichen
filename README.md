# Introduction

TinyGen is a simple coding assistant FastAPI API. After taking in an URL of a public repo on Github and a textual prompt as the command, it will return a unified diff (as a string) representing the changes to be made, with the help of ChatGPT. 

# How to use this API on the Web

To check whether the server is currently running, you can visit http://18.224.31.85:8000/ on a browser or send a GET request to this URL. If you received an emoji string, that means the server is up and running. 

To use it, send a POST request with a repoUrl (the URL of a public repo on Github) and a texual prompt to http://18.224.31.85:8000/. For example: 
{
  "repoUrl": "https://github.com/owner_name/repo_name",
  "prompt": "Please add some documentations to the code"
}

Alternatively, you can visit http://18.224.31.85:8000/docs on your browser, select the POST request and select "Try it out" to test this API. 

After some time the API will respond with the diff that accomplishes the specified task, or an error message if one occurred. The response may take a while as it relies on a ChatGPT LLM. 

# How to run it on your local machine

After cloning this repository to your local machine, you need to first configure the environment. It is recommended to create and activate a virtual environment using the following command (assuming you are on macOS):
```
python3 -m venv myenv
source myenv/bin/activate
```
Then install the required packages using 
```
pip install -r requirements.txt
```

