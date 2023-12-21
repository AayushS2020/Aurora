function search() {
    console.log('Search button clicked');
    const query = document.getElementById('textInput').value;
    const useRPSearch = document.getElementById('useRPCheckbox').checked;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${encodeURIComponent(query)}&use_rp_search=${useRPSearch}&sort_by=date:r:${getPastYearDate()}`,
    })
    .then(response => response.json())
    .then(data => displayResults(query, data.items))
    .catch(error => console.error('Error:', error));
}

function getPastYearDate() {
    const currentDate = new Date();
    const pastYear = currentDate.getFullYear() - 1;
    return `${pastYear}-${currentDate.getMonth() + 1}-${currentDate.getDate()}`;
}

function regenerateSearch(query) {
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${encodeURIComponent(query)}&use_rp_search=false&sort_by=date:r:${getPastYearDateForSearch()}`,
    })
    .then(response => response.json())
    .then(data => displayResults(query, data.items))
    .catch(error => console.error('Error:', error));
}

function getPastYearDateForSearch() {
    const currentDate = new Date();
    const pastYear = currentDate.getFullYear() - 1;
    return `${pastYear}-01-01`;  
}

function displayResults(question, items) {
    const resultsDiv = document.getElementById('chatWindow');

    // Create a new result container for each question
    const resultContainer = document.createElement('div');
    resultContainer.classList.add('message');

    // Display the user's question
    const questionElement = document.createElement('div');
    questionElement.classList.add('user-message');
    questionElement.innerHTML = `<strong>User Question:</strong> ${question}`;
    resultContainer.appendChild(questionElement);

    // Limit the number of displayed results to top 5
    const limitedItems = items.slice(0, 5);

    limitedItems.forEach(item => {
        const title = item.title;
        const snippet = item.snippet;
        const link = item.link;

        const resultElement = document.createElement('div');
        resultElement.classList.add('ai-message');
        resultElement.innerHTML = `<h3>${title}</h3><p>${snippet}</p><a href="${link}" target="_blank">${link}</a><hr>`;
        resultContainer.appendChild(resultElement);
    });

    // Add a "Regenerate Response" button
    const regenerateButton = document.createElement('div');
    regenerateButton.classList.add('regenerate-button');
    regenerateButton.innerHTML = 'Regenerate Response';
    regenerateButton.onclick = function () {
        // Trigger a new search with the same query and check the "Use RP Search" checkbox
        document.getElementById('textInput').value = question;
        document.getElementById('useRPCheckbox').checked = true;
        regenerateSearch(question);
    };
    resultContainer.appendChild(regenerateButton);

    // Append the result container to the results area
    resultsDiv.appendChild(resultContainer);

    // Clear the input field for the next question
    document.getElementById('textInput').value = '';
}
