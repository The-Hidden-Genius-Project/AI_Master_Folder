document.getElementById('promptForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const prompt = document.getElementById('prompt').value;

    const imageUrl = await fetchImage(prompt);
    displayImage(imageUrl);
});

async function fetchImage(prompt) {
    try {
        const response = await fetch('/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        const data = await response.json();
        return data.imageUrl; // The URL of the generated image
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayImage(url) {
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = `<img src="${url}" alt="Generated Image" />`;
}