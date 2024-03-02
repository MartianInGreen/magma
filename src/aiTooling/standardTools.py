### ----------------------------------------------------
### File: standardTools.py
### Authors: Hannah Renners
### ----------------------------------------------------

# ----------------------------------------------------
# Imports
# ----------------------------------------------------

import replicate
from openai import OpenAI
import litellm
from tavily import TavilyClient

import tinydb 

try: 
    from ..utils import getEnvVar
except:
    from utils import getEnvVar

import requests, bs4, os, time, json, urllib.parse, re, subprocess, uuid

### ----------------------------------------------------
### Standard Tools
### ----------------------------------------------------

# ----------------------------------------------------
# Code Interpreter
# ----------------------------------------------------

def codeInterpreter(language: str, code: str, chatId: str):
    if language not in ('python', 'nodejs', 'bash'):
        raise ValueError("Language must be either 'python' or 'nodejs' or 'bash'")
    
    runID = str(uuid.uuid4())

    os.makedirs(f"../storage/chats/{chatId}/files/", exist_ok=True)
    fileLocation = os.path.abspath(f"../storage/chats/{chatId}/files/")

    dockerCommand = f"docker run -v {fileLocation}:/runtime:rw --rm --name codeapi codeapi"

    if language == "python":
        fullCommand = dockerCommand.split(" ")
        fullCommand += ["ipython", "-c", f"{code}"]

        output = subprocess.Popen(fullCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = output.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        
        return { "stdout": stdout, "stderr": stderr }
    else: 
        return { "result": "Language not supported" }


# ----------------------------------------------------
# Generate Image
# ----------------------------------------------------

def generateImage(model: str, positivePrompt: str, negativePrompt: str, aspectRatio: str, quality: str, chatId: str = None):
    if model not in ('dall-e-3', 'sd-xl', 'proteus', 'stable-diffusion', 'playground-v2.5'):
        raise ValueError("Model not supported")
    if aspectRatio not in ('1:1', '4:5', '16:9', '3:4', '9:16'):
        raise ValueError("Aspect ratio not supported")
    if quality not in ('normal', 'high'):
        raise ValueError("Quality must be either 'normal' or 'high")
    
    if model == "dall-e-3":
        width = 1024
        height = 1024

        if aspectRatio == "1:1" or aspectRatio == "4:5" or aspectRatio == "3:4":
            width = 1024
            height = 1024
        elif aspectRatio == "16:9":
            height = 1024
            width = 1792
        elif aspectRatio == "9:16": 
            height = 1792
            width = 1024

        quality = "normal" if quality == "normal" else "hd"

        client = OpenAI(api_key=getEnvVar("OPENAI_API_KEY"))

        try:
            output = client.images.generate(
                model="dall-e-3",
                prompt=positivePrompt,
                size=str(width) + "x" + str(height),
                quality=quality,
                n=1
            )

            imageURL = output.data[0].url
            body = {
                "statusCode": 200,
                "results": imageURL
            }
        except:
            body = {
                "statusCode": 400,
                "body": "Error generating image."
            }
        
        return body
    
    elif model == "sd-xl" or model == "prometheus" or model == "stable-diffusion":
        width = 1024
        height = 1024
        if aspectRatio == "1:1":
            width = 1024
            height = 1024
        elif aspectRatio == "4:5":
            width = 1024
            height = 1280
        elif aspectRatio == "16:9":
            width = 1024
            height = 576
        elif aspectRatio == "3:4":
            width = 1024
            height = 1365
        elif aspectRatio == "9:16":
            width = 576
            height = 1024

        if model == "sd-xl":
            if quality == "hd":
                modelID = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
            else:
                modelID = "lucataco/sdxl-lightning-4step:727e49a643e999d602a896c774a0658ffefea21465756a6ce24b7ea4165eba6a"
        elif model == "proteus":
            modelID = "lucataco/proteus-v0.4-lightning:21464a198e9baa3b583f93d8daaaa9e851b91ae1e32accb96ce5081a18a2d87c"
        elif model == "stable-diffusion":
            modelID = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"
        elif model == "playground-v2.5":
            modelID = "lucataco/playground-v2.5-1024px-aesthetic:419269784d9e00c56e5b09747cfc059a421e0c044d5472109e129b746508c365"

        client = replicate.Client(getEnvVar("REPLICATE_API_KEY"))

        try: 
            output = client.run(
                modelID, 
                input={
                    "height": height,
                    "width": width,
                    "prompt": positivePrompt,
                    "negative_prompt": negativePrompt,
                    "disable_safety_checker": True
                }
            )

            body = {
                "statusCode": 200,
                "results": output
            }
        except:
            body = {
                "statusCode": 400,
                "body": "Error generating image."
            }
        
        return body

# ----------------------------------------------------
# Web Search
# ----------------------------------------------------

def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

def searchWithBrave(query: str, type: str, focus: str, freshness: str, country: str, chatId: str = None, customGoggles: str = None):
    if type not in ('quick', 'deep', 'research'):
        raise ValueError("Type must be either 'quick' or 'deep' or 'research'")
    if focus not in ('all', 'web', 'news', 'reddit', 'academia', 'video'):
        raise ValueError("Focus must be either 'all' or 'web' or 'news' or 'reddit' or 'academia' or 'video'")
    if freshness not in ('24h', 'week', 'month', 'year', 'all'):
        raise ValueError("Freshness must be either '24h' or 'week' or 'month' or 'year' or 'all'")
    if country.__len__() != 2:
        raise ValueError("Country must be a two letter country code")
    
    # Define the brave search function
    def searchBrave(query: str, type: str, focus: str, freshness: str, country: str):
        results_filter = "infobox"
        # Focus is ["web", "news", "reddit", "video", "all"]
        if focus == "web" or focus == "all":
            results_filter += ",web"
        if focus == "news" or focus == "all":
            results_filter += ",news"
        if focus == "video":
            results_filter += ",videos"

        # Handle focuses that use goggles
        goggles_id = ""
        if focus == "reddit":
            goggles_id = "&goggles_id=https://raw.githubusercontent.com/mrmathew/brave-search-goggle/main/reddit-search"
        elif focus == "academia":
            goggles_id = "&goggles_id=https://raw.githubusercontent.com/solso/goggles/main/academic_papers_search.goggle"

        # Handle custom goggles
        if customGoggles:
            goggles_id = "&goggles_id=" + customGoggles

        freshness = ""
        # Handle Freshness
        if freshness == "24h":
            freshness = "&freshness=pd"
        elif freshness == "week":
            freshness = "&freshness=pw"
        elif freshness == "month":
            freshness = "&freshness=pm"
        elif freshness == "year":
            freshness = "&freshness=py"
        elif freshness == "all":
            freshness = ""

        encoded_query = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_query}&results_filter=i{results_filter}&country={country}&search_lang=en&text_decorations=no&extra_snippets=true&count=20" + freshness + goggles_id
        print(url)
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": getEnvVar("BRAVE_SEARCH_API_KEY")
        }

        try:
            start_search = time.time()
            print("Getting brave search results...")
            response = requests.get(url, headers=headers)
            data = response.json()
            end_search = time.time()
            search_time = end_search - start_search
            print("Brave search took: " + str(end_search - start_search) + " seconds")
        except:
            return {
                'statusCode': 400,
                'body': json.dumps('Error fetching search results.')
            }
        
        def decode_data(data):
            results = []

            for result in data["web"]["results"]:
                url = result.get("profile", {}).get("url", result.get("url", "could not find url"))
                description = remove_html_tags(result.get("description", ""))

                deep_results = []
                for snippet in result.get("extra_snippets", []):
                    cleaned_snippet = remove_html_tags(snippet)
                    deep_results.append({"snippets": cleaned_snippet})

                result_entry = {
                    "description": description,
                    "url": url,
                }

                if deep_results:
                    result_entry["deep_results"] = deep_results

                results.append(result_entry)
            return results

        results = decode_data(data)
        return results

    try: 
        results = searchBrave(query, type, focus, freshness, country)
        return results
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching search results.')
        }

def searchWithTravily(query: str, search_depth: str = "advanced", chatId: str = None) -> dict:
    travily = TavilyClient(getEnvVar("TRAVILY_API_KEY")) 

    if search_depth != "advanced" and search_depth != "basic":
        raise ValueError("Search depth must be either 'advanced' or 'basic'")
    
    response = travily.search(query, search_depth)

    context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]

    return {
        "statusCode": 200,
        "results": context
    }

def webScrape(url: str, type: str, modelName: str, chatId: str = None):
    if type not in ('full', 'summary'):
        raise ValueError("Type must be either 'quick' or 'deep' or 'research'")
    
    def scrapeURL(url: str):
        scrape_url = f"https://api.scrapingrobot.com/?token={getEnvVar('SCRAPING_ROBOT_TOKEN')}&render=false&proxyCountry=US&url={url}"

        try:
            scrape_response = requests.post(scrape_url, headers={"Accept": "application/json"}, timeout=12)
        except:
            print("Could not scrape page (timeout)...")
            return {"url": str(url), "text": "No data..."}
        
        try:
            scrape_data = scrape_response.json()
        except:
            print("Could not scrape page (no json)...")
            return {"url": str(url), "text": "No data..."}
        
        if "result" in scrape_data:
            scrape_data = scrape_data["result"]
        else:
            print("Could not scrape page (no results)...")
            return {"url": str(url), "text": "No data..."}
        
        text = remove_html_tags(scrape_data)
        text = text.replace("\n", " ")
        text.encode('utf-8')
        text = text.encode('ascii', 'ignore').decode('ascii')

        return text

    def scrapeSummary(url: str, modelName: str):
        modelDB = tinydb.TinyDB('../storage/models.json')
        models = modelDB.table('models')

        # Check if model exists
        models = models.search(tinydb.where('name') == modelName)
        if not models:
            return {"url": str(url), "text": "No data... (Model not found)"}
        
        # Get model
        try: 
            model = models[0]
            modelName = model['modelName']
            apiKey = model['llmParams']['apiKey']
        except:
            return {"url": str(url), "text": "No data... (Model not found)"}
        
        # Scrape the page
        text = scrapeURL(url)

        response = litellm.completion(
            model=modelName,
            apiKey=apiKey,
            messages=[
                {
                    "role": "system",
                    "content": "You are a research and search assistant designed to help users find information on the internet by summarizing web pages. Answer in about 500 to 1000 Words.",
                },
                {
                    "role": "user",
                    "content": "Web page: \n\n\n" + text,
                }
            ]
        )

        try: 
            message = response.choices[0].message.content
        except:
            return {"url": str(url), "text": "No data... (Model error)"}

        return message

    def scrapeReddit():
        pass

    def scrapeYoutube():
        pass

    if type == "full":
        response = {
            "url": url,
            "text": scrapeURL(url)
        }
        return response
    elif type == "summary":
        response = {
            "url": url,
            "text": scrapeSummary(url, modelName)
        }
        return response

# ----------------------------------------------------
# Wolfram|Alpha
# ----------------------------------------------------
    
def wolframAlpha(query: str, chatId: str = None):
    # baseURL = f"http://api.wolframalpha.com/v2/query?appid={getEnvVar('WOLFRAM_APP_ID')}&output=json&input="
    baseURL = f"https://www.wolframalpha.com/api/v1/llm-api?appid={getEnvVar('WOLFRAM_APP_ID')}&input="

    # Encode the query
    encoded_query = urllib.parse.quote(query)
    url = baseURL + encoded_query

    try:
        response = requests.get(url)
        print(response)
        data = response.text
        print(str(data))
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching Wolfram|Alpha results.')
        }
    
    return {
        'statusCode': 200,
        'results': json.dumps(data)
    }

# ----------------------------------------------------
# Files
# ----------------------------------------------------

def readTextFile(file_name: str, chatId: str):
    # See if file ends with .txt, .md, .html, .json, .csv, .xml, .yaml
    file_ending = file_name.split(".")[-1]
    if file_ending not in ('txt', 'md', 'html', 'json', 'csv', 'xml', 'yaml', 'pdf'):
        raise ValueError("File type not supported")
    
    # Read the file
    file_path = f"../storage/chats/{chatId}/files/{file_name}"

    try:
        # if file_ending == "pdf":
        #     with open(file_path, 'rb') as f:
        #         reader = pyPDF2.PdfReader(f)
        #         text = ""
        #         for page in reader.pages:
        #             text += page.extract_text()
        #else:
        with open(file_path, 'r') as f:
            text = f.read()
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error reading file.')
        }
    
    return { 'file': file_name, 'text': text }

def askPDF(file_name: str, query: str, chatId: str):
    pass

if __name__ == "__main__":
    print(wolframAlpha("What is the capital of France?"))