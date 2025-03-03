const express = require('express');
const fetch = require('node-fetch');
require('dotenv').config();

const app = express();
app.use(express.json());

const OPENAI_API_KEY = "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";

app.post('/generate-image', async (req, res) => {
    const { prompt } = req.body;

    try {
        const response = await fetch('https://api.openai.com/v1/images/generations', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                n: 1, // Number of images to generate
                size: "1024x1024" // Image size
            })
        });

        const data = await response.json();
        const imageUrl = data.data[0].url;
        res.json({ imageUrl });
    } catch (error) {
        console.error('Error generating image:', error);
        res.status(500).send('Error generating image');
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});