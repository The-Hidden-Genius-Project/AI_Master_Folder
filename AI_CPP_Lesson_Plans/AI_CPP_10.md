<img src="https://github.com/Hgp-GeniusLabs/Curriculum/blob/10734f2c827128dde773ea4f266d154d46977866/Org-Wide/Assets/hgp_logo_original.png" width="150"/>

# LESSON 10: AI Recap

## Overview			
* Understand the basics of AI
* See how AI shapes our future
* Learn how to maneuver around the world of AI
* Learn different components that make up AI
* Work with real world AI Applications

## Learning Activities and Time Duration(2 hours) 

1. Watch video on AI

2. Recap on funniest activities

7. Code in replit abstract artwork builder:

Download needed files in shell
```
pip install numpy
pip install pillow

Main code for replit
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def generate_random_artwork(image_path='random_artwork.png',
                            width=800,
                            height=600,
                            num_elements=50):
    # Create a blank canvas
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    for _ in range(num_elements):
        element_type = random.choice(
            ['circle', 'rectangle', 'line', 'ellipse'])

        # Random position and size
        x0 = random.randint(0, width)
        y0 = random.randint(0, height)
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)

        # Ensure x1 > x0 and y1 > y0
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        # Random color
        color = tuple(np.random.randint(0, 256, size=3))

        # Draw the element
        if element_type == 'circle':
            bbox = [x0, y0, x1, y1]
            draw.ellipse(bbox, fill=color, outline=color)
        elif element_type == 'rectangle':
            bbox = [x0, y0, x1, y1]
            draw.rectangle(bbox, fill=color, outline=color)
        elif element_type == 'line':
            draw.line([x0, y0, x1, y1],
                      fill=color,
                      width=random.randint(1, 10))
        elif element_type == 'ellipse':
            bbox = [x0, y0, x1, y1]
            draw.ellipse(bbox, fill=color, outline=color)

    # Save the image
    image.save(image_path)
    print(f"Random artwork saved at {image_path}")


# Example usage
if __name__ == "__main__":
    generate_random_artwork()
```

* Work more on chatbot
