document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.getElementById('start-training-btn');
    const statusDiv = document.getElementById('training-status');

    startBtn.addEventListener('click', function () {
        startBtn.disabled = true;
        statusDiv.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Model Training...</span></div> Training in progress...';

        fetch('/start_training', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Training started') {
                const interval = setInterval(() => {
                    fetch('/training_status')
                        .then(res => res.json())
                        .then(statusData => {
                            if (statusData.status === 'Training complete') {
                                clearInterval(interval);
                                statusDiv.innerHTML = '<span class="badge bg-success animate__animated animate__fadeIn">🎉 The model is ready for use!</span>';

                                const generateBtn = document.createElement('button');
                                generateBtn.className = 'btn btn-success btn-lg mt-3 animate__animated animate__fadeIn';
                                generateBtn.innerText = 'Proceed to correct the text';
                                generateBtn.onclick = () => {
                                    window.location.href = '/autocorrect';
                                };
                                statusDiv.appendChild(generateBtn);
                            } else if (statusData.status === 'Training in progress') {

                                statusDiv.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Model Training...</span></div> Training in progress...';
                            } else {
                                clearInterval(interval);
                                statusDiv.innerHTML = '<span class="badge bg-danger animate__animated animate__shakeX">Error during training</span>';
                                startBtn.disabled = false;
                            }
                        });
                }, 3000);
            } else {
                statusDiv.innerHTML = '<span class="badge bg-warning animate__animated animate__pulse">The training is already in progress.</span>';
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            statusDiv.innerHTML = '<span class="badge bg-danger animate__animated animate__shakeX">Error starting the training</span>';
            startBtn.disabled = false;
        });
    });
});
