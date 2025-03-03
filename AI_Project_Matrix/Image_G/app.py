from openai import OpenAI

client = OpenAI(api_key='ADD API Key')

import requests

from PIL import Image

from io import BytesIO



# Set the OpenAI API key




def generate_image(prompt):

    try:

        response = client.images.generate(prompt=prompt,
        
        n=1,
        
        size="1024x1024")

        image_url = response.data[0].url

        return image_url

    except Exception as e:

        print(f"Error generating image: {e}")

        return None



def generate_caption(image_description):

    messages = [

        {"role": "system", "content": "You are a creative assistant."},

        {"role": "user", "content": f"Generate a creative caption for an image described as follows: {image_description}"}

    ]



    try:

        response = client.chat.completions.create(model="gpt-4",  # Use GPT-4 model identifier
        
        messages=messages,
        
        max_tokens=50,
        
        temperature=1.0)

        caption = response.choices[0].message.content.strip()

        return caption

    except Exception as e:

        print(f"Error generating caption: {e}")

        return None



def main():

    image_prompt = "image the Golden State without words"



    image_url = generate_image(image_prompt)

    if image_url:

        print(f"Generated Image URL: {image_url}")



        image_description = "A beautiful futuristic cityscape during sunset with flying cars in the sky, blending technology with natural beauty."

        caption = generate_caption(image_description)



        if caption:

            print(f"Generated Caption: {caption}")



        response = requests.get(image_url)

        img = Image.open(BytesIO(response.content))

        img.show()

    else:

        print("Failed to generate image.")



if __name__ == "__main__":

    main()
