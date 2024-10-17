document.addEventListener('DOMContentLoaded', function () {
    const checkButton = document.getElementById('checkButton');
    const textInput = document.getElementById('textInput');
    const correctedTextArea = document.getElementById('correctedText');

    async function processWords(words, currentIndex = 0) {
        if (currentIndex >= words.length) {
            correctedTextArea.value = words.join(' '); 
            return; 
        }

        const currentText = words.slice(0, currentIndex + 1).join(' '); 
        try {
            const response = await fetch('/autocorrect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: currentText }),
            });

            if (response.ok) {
                const data = await response.json();
                const correctedWords = data.corrected_text.split(' ');

                words[currentIndex] = correctedWords[currentIndex];

                processWords(words, currentIndex + 1);
            } else {
                console.error('Error during correction');
            }
        } catch (error) {
            console.error('Error during the request:', error);
        }
    }

    checkButton.addEventListener('click', async () => {
        const userInput = textInput.value.trim();
        correctedTextArea.value = '';

        const words = userInput.split(/\s+/); 

        processWords(words);
    });
});
