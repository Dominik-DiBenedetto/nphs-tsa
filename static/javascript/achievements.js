const placementsData = [
    {
        year: 2025,
        conferences: [
            {
                name: "Manatee Regionals",
                location: "Bradenton, FL",
                date: "December 14, 2024",
                placements: [
                    { event: "Chapter Team", students: "Dominik DiBenedetto, Isabella Ramsey, Matthew Jakoby, Chaz LaFlair, Joseph Carlo-Tsourakis, Megan Taylor", rank: "2nd" },
                ]
            },
            {
                name: "Florida State Conference",
                location: "Orlando, FL",
                date: "February 19-23, 2025",
                placements: [
                    { event: "Biotechnology Design", students: "Megan Taylor", rank: "3rd" },
                    { event: "Coding", students: "Dominik DiBenedetto, Gavin Arsenault", rank: "1st" },
                    { event: "Debating Technology Issues", students: "Isabella Ramsey, Mya Bright", rank: "1st" },
                    { event: "Drone Challenge", students: "Matthew Jakoby", rank: "1st" },
                    { event: "Extempraneous Speech", students: "Alexander Avin", rank: "3rd" },
                    { event: "Fashion Design and Technology", students: "Elizabeth Carpenter, Michael Dankanich, Savannah Wilmer", rank: "3rd" },
                    { event: "Forensics Science", students: "Savannah Wilmer", rank: "3rd" },
                    { event: "Prepared Presentation", students: "Megan Taylor", rank: "1st" },
                    { event: "Technology Problem Solving", students: "Matthew Jakoby, Elizabeth Carpenter", rank: "1st" },
                    { event: "Video Game Design", students: "Dominik DiBenedetto, Alexander Avin, Michael Dankanich, Huy Nguyen, Aditya Warrier", rank: "2nd" },
                    { event: "Virtual Reality Simulation", students: "Dominik DiBenedetto, Michael Dankanich, Huy Nguyen, Chaz LaFlair", rank: "2nd" }
                ]
            },
            {
                name: "Nationals",
                location: "Nashville, TN",
                date: "June 27-July 1, 2025",
                placements: [
                    { event: "Geospatial Technology", students: "Aditya Warrier, Alexander Avin, Matthew Jakoby", rank: "1st" },
                ]
            }
        ]
    },
    {
        year: 2024,
        conferences: [
            {
                name: "Manatee Regionals",
                location: "Bradenton, FL",
                date: "December, 2023",
                placements: [
                    
                ]
            },
            {
                name: "Florida State Conference",
                location: "Orlando, FL",
                date: "February 19-23, 2022",
                placements: [
                    { event: "Geospatial Technology", students: "Hannah Aguilar", rank: "1st" },
                    { event: "Prepared Presentation", students: "Megan Taylor", rank: "2nd" },
                    { event: "Promotional Design", students: "", rank: "3rd" },
                    { event: "Virtual Reality Simulation", students: "Chaz LaFlair, Joseph Carlo-Tsourakis, Zander Hilton", rank: "3rd" },
                ]
            },
            {
                name: "Nationals",
                location: "Orlando, FL",
                date: "June 27-July 1, 2022",
                placements: [
                    
                ]
            }
        ]
    },
];

let filteredData = [...placementsData];

// Initialize the page
function init() {
    populateFilters();
    renderPlacements();
    updateStats();
    setupEventListeners();
}

// Populate filter dropdowns
function populateFilters() {
    const years = [...new Set(placementsData.map(item => item.year))].sort((a, b) => b - a);
    const conferences = [...new Set(placementsData.flatMap(item => 
        item.conferences.map(conf => conf.name)
    ))].sort();
    const companies = [...new Set(placementsData.flatMap(item => 
        item.conferences.flatMap(conf => 
            conf.placements.map(placement => placement.students)
        )
    ))].sort();

    populateSelect('yearFilter', years);
    populateSelect('conferenceFilter', conferences);
}

function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
}

// Render placements
function renderPlacements() {
    const container = document.getElementById('placementsContent');
    const noResults = document.getElementById('noResults');

    if (filteredData.length === 0) {
        container.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }

    noResults.style.display = 'none';
    container.innerHTML = '';

    filteredData.forEach((yearData, index) => {
        const yearSection = createYearSection(yearData, index);
        container.appendChild(yearSection);
    });
}

function createYearSection(yearData, index) {
    const section = document.createElement('div');
    section.className = 'year-section fade-in';
    section.style.animationDelay = `${index * 0.1}s`;

    const totalPlacements = yearData.conferences.reduce((sum, conf) => sum + conf.placements.length, 0);

    section.innerHTML = `
        <div class="year-header" onclick="toggleYear(this)">
            <div class="year-title">${yearData.year}</div>
            <div class="year-count">${totalPlacements} placements</div>
            <div class="toggle-icon">▼</div>
        </div>
        <div class="conferences-container">
            ${yearData.conferences.map(conf => createConferenceCard(conf)).join('')}
        </div>
    `;

    return section;
}

function createConferenceCard(conference) {
    return `
        <div class="conference-card">
            <div class="conference-header">
                <div>
                    <div class="conference-name">${conference.name}</div>
                    <div class="conference-location">📍 ${conference.location}</div>
                </div>
                <div class="conference-date">${conference.date}</div>
            </div>
            <div class="placements-list">
                ${conference.placements.map(placement => `
                    <div class="placement-item">
                        <div class="placement-info">
                            <div class="event-name">${placement.event}</div>
                            <div class="students-name">${placement.students}</div>
                        </div>
                        <div class="placement-rank">${placement.rank}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Toggle year section
function toggleYear(header) {
    const section = header.parentElement;
    section.classList.toggle('collapsed');
}

// Update statistics
function updateStats() {
    const totalPlacements = filteredData.reduce((sum, year) => 
        sum + year.conferences.reduce((confSum, conf) => confSum + conf.placements.length, 0), 0
    );
    const totalConferences = filteredData.reduce((sum, year) => sum + year.conferences.length, 0);
    const companies = new Set(filteredData.flatMap(year => 
        year.conferences.flatMap(conf => 
            conf.placements.map(placement => placement.students)
        )
    ));
    const totalYears = filteredData.length;

    document.getElementById('totalPlacements').textContent = totalPlacements;
    document.getElementById('totalConferences').textContent = totalConferences;
    document.getElementById('totalCompanies').textContent = companies.size;
    document.getElementById('totalYears').textContent = totalYears;
}

// Filter functions
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const yearFilter = document.getElementById('yearFilter').value;
    const conferenceFilter = document.getElementById('conferenceFilter').value;

    filteredData = placementsData.map(yearData => {
        // Filter by year
        if (yearFilter && yearData.year.toString() !== yearFilter) {
            return null;
        }

        const filteredConferences = yearData.conferences.map(conference => {
            // Filter by conference
            if (conferenceFilter && conference.name !== conferenceFilter) {
                return null;
            }

            const filteredPlacements = conference.placements.filter(placement => {

                // Filter by search term
                if (searchTerm) {
                    const searchableText = `${placement.event} ${placement.students} ${placement.rank}`.toLowerCase();
                    if (!searchableText.includes(searchTerm)) {
                        return false;
                    }
                }

                return true;
            });

            if (filteredPlacements.length === 0) {
                return null;
            }

            return {
                ...conference,
                placements: filteredPlacements
            };
        }).filter(conf => conf !== null);

        if (filteredConferences.length === 0) {
            return null;
        }

        return {
            ...yearData,
            conferences: filteredConferences
        };
    }).filter(year => year !== null);

    renderPlacements();
    updateStats();
}

function clearAllFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('yearFilter').value = '';
    document.getElementById('conferenceFilter').value = '';
    
    filteredData = [...placementsData];
    renderPlacements();
    updateStats();
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', applyFilters);
    document.getElementById('yearFilter').addEventListener('change', applyFilters);
    document.getElementById('conferenceFilter').addEventListener('change', applyFilters);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);