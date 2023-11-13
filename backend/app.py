from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:3000",  # React app running on localhost:3000
    "http://localhost:3001",
    # "http://yourfrontenddomain.com",  # Your production frontend domain
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)
llm = "gpt-3.5-turbo"

class ProductInfo(BaseModel):
    name: str
    description: str

@app.post("/generate_script")
def generate_script(product_info: ProductInfo):
    try:
        messages = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }, {
            "role":
            "user",
            "content":
            f"Generate three script ideas for a testimonial video ad, focusing on the product {product_info.name}, {product_info.description}. The ad should be 30 seconds long and target customers of all age. We want the tone to be light-hearted yet convincing. Each script should highlight SuperCleaner 3000's ease of use and effectiveness, and include our slogan 'Sparkle in a Spray'. Please use the screenplay format suitable for TV and ensure each idea offers a unique approach, possibly exploring different customer experiences. Note: The product name must be mentioned at least thrice in the script."
        }]
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",  # Adjust model as necessary
            model=llm,  # Adjust model as necessary
            messages=messages,
            # max_tokens=150  # You can adjust this
            max_tokens=500  # You can adjust this
        )
        # Accessing the generated script
        generated_script = response.choices[
            0].message.content if response.choices[
                0].message else "No script generated."
        return generated_script
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check_api_health")
def check_api_health():
    try:
        response = client.chat.completions.create(model=llm,
                                                  messages=[{
                                                      "role":
                                                      "system",
                                                      "content":
                                                      "This is a test"
                                                  }])
        print(response)
    except Exception as e:
        return {"Error": str(e), "API key is valid": False}
    else:
        return {"API key is valid": True}


# Mount the React build folder as a static files directory
app.mount("/",
          StaticFiles(directory="../frontend/build", html=True),
          name="static")

# You can then run this application using Uvicorn from the command line:
# uvicorn filename:app --reload
