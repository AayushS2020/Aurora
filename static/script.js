function search() {
    const query = document.getElementById('query').value;
    const useRPSearch = document.getElementById('useRP').checked;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${encodeURIComponent(query)}&use_rp_search=${useRPSearch}`,
    })
    .then(response => response.json())
    .then(data => displayResults(query, data.items))  // Pass the user's question to displayResults
    .catch(error => console.error('Error:', error));
}

function displayResults(question, items) {
    const resultsDiv = document.getElementById('resultsArea');

    // Create a new result container for each question
    const resultContainer = document.createElement('div');
    resultContainer.classList.add('result-box', 'mt-4', 'mb-4');  // Add margin-bottom

    // Display the user's question
    const questionElement = document.createElement('div');
    questionElement.classList.add('user-question');
    questionElement.innerHTML = `<strong>User Question:</strong> ${question}`;
    resultContainer.appendChild(questionElement);

    // Limit the number of displayed results to top 5
    const limitedItems = items.slice(0, 5);

    limitedItems.forEach(item => {
        const title = item.title;
        const snippet = item.snippet;
        const link = item.link;

        const resultElement = document.createElement('div');
        resultElement.innerHTML = `<h3>${title}</h3><p>${snippet}</p><a href="${link}" target="_blank">${link}</a><hr>`;
        resultContainer.appendChild(resultElement);
    });

    // Append the result container to the results area
    resultsDiv.appendChild(resultContainer);

    // Clear the input field for the next question
    document.getElementById('query').value = '';
}



