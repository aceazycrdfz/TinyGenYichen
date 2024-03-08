from urllib.parse import urlparse
import requests
import base64

def extract_owner_repo(github_url):
    """
    Extracts the owner and repository name from a GitHub URL.

    :param github_url: The full URL to a GitHub repository.
    :return: A tuple containing the owner and repository name.
    """
    parsed_url = urlparse(github_url)
    path = parsed_url.path

    # Split the path to get the owner and repo names
    _, owner, repo, *_ = path.split('/')

    return owner, repo

def fetch_file_contents(owner, repo, path=''):
    """
    Fetches the contents of files in a GitHub repository.

    :param owner: The owner of the repository.
    :param repo: The repository name.
    :param path: The path within the repository (default is root).
    :return: A list of tuples, each containing the file path and its content.
    """
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(api_url)
    files_info = []  # Will hold tuples of (file_path, file_content)

    if response.status_code == 200:
        contents = response.json()
        for content in contents:
            if content['type'] == 'file':
                file_content = requests.get(content['download_url']).text
                file_path = content['path']
                files_info.append((file_path, file_content))
            elif content['type'] == 'dir':
                # Recursively fetch contents from the directory
                directory_contents = fetch_file_contents(owner, repo, content['path'])
                files_info.extend(directory_contents)

    return files_info

# Read the API key from api_key.txt
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip() # .strip() removes any leading/trailing whitespace

def call_chatgpt(github_url, prompt_instruction):
    """
    Asks ChatGPT for help with the public github repo 
    and returns the response as unified diff.

    :param github_url: The URL of the repository.
    :param prompt_instruction: The instruction.
    :return: A string, the response/error message.
    """
    owner, repo = extract_owner_repo(github_url)
    # a list of (file_path, file_content) tuples
    all_files_info = fetch_file_contents(owner, repo)
    
    # things to be sent to ChatGPT
    sys_instruction = """
    You are a helpful coding assistant. 
    You will be given all the files from a github repository. 
    The file names/paths will be given one by one. 
    At the end there will be an instruction. Please follow the intruction to modify the code. 
    Please return a unified diff (as a string) representing the changes to be made
    """
    messages = [{"role": "system", "content": sys_instruction}]
    
    for file_path, file_content in all_files_info:
        msg_content = f'File Path: {file_path}\nFile Content: {file_content}'
        messages.append({"role": "user", "content": msg_content})
    
    final_instruction = "Remember please only return a unified diff (as a string) representing the changes to be made"
    messages.append({"role": "user", 
                     "content": prompt_instruction+final_instruction})
    
    endpoint = "https://api.openai.com/v1/chat/completions"
    model="gpt-3.5-turbo-0125"
    data = {
      "model": model,
      "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response1 = requests.post(endpoint, json=data, headers=headers)
    if response1.status_code == 200:
        print(response1.json()["choices"][0]["message"]["content"])
    else:
        print("Error:", response1.text)
    
    
    messages.append({"role": "assistant", 
                     "content": response1.json()["choices"][0]["message"]["content"]})
    reflection_instruction = """
    Are you sure about your answer? Can you do better?
    If so please offer a better answer, otherwise repeat your previous response
    """
    messages.append({"role": "user", 
                     "content": reflection_instruction})
    
    response2 = requests.post(endpoint, json=data, headers=headers)
    if response2.status_code == 200:
        print(response2.json()["choices"][0]["message"]["content"])
    else:
        print("Error:", response2.text)


github_url = 'https://github.com/aceazycrdfz/YouTubeDownloaderGUI'
prompt_instruction = "Please add relevant documentations"



