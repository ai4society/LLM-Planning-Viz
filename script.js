document.addEventListener('DOMContentLoaded', () => {
    const categoryLinks = document.querySelectorAll('.category-list a');

    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const category = e.target.getAttribute('data-category');
            displayPapers(category);
        });
    });
});

function displayPapers(category) {
    const papersContainer = document.getElementById('papers-container');
    const filteredPapers = papersData.filter(paper => paper.category === category);

    // Sort papers in descending order by year
    filteredPapers.sort((a, b) => parseInt(b.year) - parseInt(a.year));

    let papersHTML = '';
    if (filteredPapers.length) {
        papersHTML += '<div class="papers-list">'; // Use a simple div container for papers

        filteredPapers.forEach((paper) => {
            papersHTML += `
                <div class="paper-entry">
                    <div class="paper-content">
                        <h4><a href="${paper.link}" target="_blank">${paper.title}</a></h4>
                        <p>${paper.authors}</p>
                        <span class="paper-year">${paper.year}</span> <!-- Optionally display the year -->
                    </div>
                </div>
            `;
        });

        papersHTML += '</div>';
    } else {
        papersHTML += '<p>No papers available for this category.</p>';
    }
    papersContainer.innerHTML = papersHTML;
}
