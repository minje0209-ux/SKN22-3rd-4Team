// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const analyzeButton = document.querySelector('.analyze-button');
    const tags = document.querySelectorAll('.tag');

    // Analyze button click handler
    analyzeButton.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query) {
            // TODO: Implement search functionality
            console.log('Analyzing:', query);
            alert(`'${query}'에 대한 AI 분석을 시작합니다!`);
        }
    });

    // Enter key handler for search input
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeButton.click();
        }
    });

    // Tag click handlers
    tags.forEach(tag => {
        tag.addEventListener('click', function() {
            const tagText = this.textContent;
            searchInput.value = tagText;
            // Optionally trigger search automatically
            // analyzeButton.click();
        });
    });
});
