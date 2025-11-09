document.addEventListener("DOMContentLoaded", () => {
  const categoryLinks = document.querySelectorAll(".category-list a");

  categoryLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const category = e.target.getAttribute("data-category");
      displayPapers(category);
    });
  });
});

function displayPapers(category) {
  const papersContainer = document.getElementById("papers-container");

  // Use the appropriate dataset based on the current year
  // If currentYear is defined in index.html, use it; otherwise default to 2025
  const papers =
    typeof currentYear !== "undefined" && currentYear === "2024" ? papersData : papersDataNew;
  const filteredPapers = papers.filter((paper) => paper.category === category);

  // Sort papers in descending order by year
  filteredPapers.sort((a, b) => parseInt(b.year) - parseInt(a.year));

  // Build a quick lookup for old papers if in 2025
  const oldTitles = new Set();
  if (typeof currentYear !== "undefined" && currentYear === "2025") {
    papersData.forEach((p) => {
      oldTitles.add(p.title.trim().toLowerCase());
    });
  }

  const newBadgeTitle =
    typeof NEW_DATE_RANGES !== "undefined" && NEW_DATE_RANGES[currentYear]
      ? NEW_DATE_RANGES[currentYear].tooltip
      : "";

  let papersHTML = "";
  if (filteredPapers.length) {
    papersHTML += '<div class="papers-list">'; // Use a simple div container for papers

    filteredPapers.forEach((paper) => {
      const isNew =
        typeof currentYear !== "undefined" &&
        currentYear === "2025" &&
        !oldTitles.has(paper.title.trim().toLowerCase());

      papersHTML += `
                <div class="paper-entry">
                    <div class="paper-content">
                        <h4>
                            <a href="${paper.link}" target="_blank">${paper.title}</a>
                            ${
                              isNew
                                ? '<span class="new-paper-badge" title="' +
                                  newBadgeTitle +
                                  '">NEW</span>'
                                : ""
                            }
                        </h4>
                        <p>${paper.authors}</p>
                        <span class="paper-year">${
                          paper.year
                        }</span> <!-- Optionally display the year -->
                    </div>
                </div>
            `;
    });

    papersHTML += "</div>";
  } else {
    papersHTML += "<p>No papers available for this category.</p>";
  }
  papersContainer.innerHTML = papersHTML;
}
