// static/js/analyze_text.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded, initializing analyze_text.js');
    const analysisSections = document.querySelectorAll('.analysis-section');
    console.log(`Found ${analysisSections.length} analysis sections`);

    analysisSections.forEach((section, index) => {
        console.log(`Initializing analysis section ${index + 1}`);
        const analyzeButton = section.querySelector('.analyze-text-button');
        const extractedText = section.querySelector('.extracted-text');
        const analysisResult = section.querySelector('.analysis-result');

        if (analyzeButton && extractedText && analysisResult) {
            console.log(`Analysis section ${index + 1} has all required elements`);
            analyzeButton.addEventListener('click', function() {
                console.log('Analyze button clicked');
                const selectedText = window.getSelection().toString().trim();
                const analysisId = this.dataset.analysisId;
                const educationLevel = this.dataset.educationLevel || 'undergraduate';
                console.log(`Education Level: ${educationLevel}`);

                console.log(`Selected text: ${selectedText.substring(0, 50)}...`);
                console.log(`Analysis ID: ${analysisId}`);
                console.log(`Education Level: ${educationLevel}`);

                if (!selectedText) {
                    console.warn('No text selected');
                    alert('Please select some text to analyze.');
                    return;
                }

                // Show loading indicator
                analysisResult.innerHTML = 'Analyzing...';

                // Make AJAX request to the server
                console.log('Sending analysis request to server');
                fetch(`/research-assistant/project/${getProjectId()}/analyze`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...(getCsrfToken() ? { 'X-CSRFToken': getCsrfToken() } : {})
                    },
                    body: JSON.stringify({
                        analysis_id: analysisId,
                        selected_text: selectedText,
                        education_level: educationLevel
                    })
                })
                    .then(response => {
                        console.log(`Server response status: ${response.status}`);
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Analysis data received:', data);
                        // Update the analysis result on the page
                        analysisResult.innerHTML = `
                        <h3>Summary:</h3>
                        <p>${data.summary}</p>
                        <h3>Research Topics:</h3>
                        <ul>
                            ${data.research_topics.map(topic => `<li>${topic}</li>`).join('')}
                        </ul>
                    `;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        analysisResult.innerHTML = 'An error occurred while analyzing the text.';
                    });
            });
        } else {
            console.warn(`Analysis section ${index + 1} is missing some elements`);
        }
    });
});

function getProjectId() {
    // Extract project ID from the current URL
    const pathParts = window.location.pathname.split('/');
    const projectId = pathParts[pathParts.indexOf('project') + 1];
    console.log(`Project ID: ${projectId}`);
    return projectId;
}

function getCsrfToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    if (tokenMeta) {
        const token = tokenMeta.getAttribute('content');
        console.log(`CSRF Token: ${token.substring(0, 5)}...`);
        return token;
    } else {
        console.warn('CSRF token meta tag not found');
        return null;
    }
}
