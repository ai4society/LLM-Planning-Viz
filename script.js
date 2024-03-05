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

    // Ensure sorting is in descending order by year
    filteredPapers.sort((a, b) => parseInt(b.year) - parseInt(a.year));

    // Group papers by year
    const papersByYear = filteredPapers.reduce((acc, paper) => {
        (acc[paper.year] = acc[paper.year] || []).push(paper);
        return acc;
    }, {});

    let papersHTML = '';
    if (filteredPapers.length) {
        papersHTML += '<div class="timeline">';

        // Initialize variable to keep track of the side
        let currentSide = 'left';

        // Ensure we are iterating through the years in descending order
        Object.keys(papersByYear).sort((a, b) => parseInt(b) - parseInt(a)).forEach(year => {
            papersHTML += `<div class="time-label" data-year="${year}">${year}</div>`; // Year label
            papersByYear[year].forEach((paper, index) => {
                papersHTML += `
                    <div class="container ${currentSide}" data-year="${year}">
                        <div class="content">
                            <h4><a href="${paper.link}" target="_blank">${paper.title}</a></h4>
                            <p>${paper.authors}</p>
                        </div>
                    </div>
                `;
            });

            // Alternate side for the next year
            currentSide = currentSide === 'left' ? 'right' : 'left';
        });

        papersHTML += '</div>';
    } else {
        papersHTML += '<p>No papers available for this category.</p>';
    }
    papersContainer.innerHTML = papersHTML;
}







