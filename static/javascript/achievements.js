let placementsData = [
    
];



let filteredData = [...placementsData];

// Initialize the page
async function init() {
    await fetch("/achievements/get_achievements/").then(res => res.json())
    .then(data => {
        placementsData = data
        filteredData = [...placementsData]
    })
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

const modal = document.querySelector(".modal")
const modalCover = document.querySelector(".modal-cover")
const modalInput = document.querySelector(".modal-input")
const modalLabel = document.querySelector(".modal-label")
const modalButton = document.querySelector(".modal-btn")
function promptAddYear() {
    modal.classList.remove("hidden")
    modalCover.classList.remove("hidden")

    modalButton.removeEventListener("click")
    modalButton.addEventListener("click", addYear)
}

function addYear(e){
    e.preventDefault();

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
            ${yearData.conferences.map(conf => createConferenceCard(conf, yearData.year)).join('')}
            <button class="add-conference-btn" onclick="openAddConferenceModal(${yearData.year})">
                ➕ Add New Conference
            </button>
        </div>
    `;

    return section;
}

function createConferenceCard(conference, year) {
    return `
        <div class="conference-card" data-year="${year}" data-conference="${conference.name}">
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
                <button class="add-placement-btn" onclick="openAddPlacementModal('${year}', '${conference.name}')">
                    ➕ Add Placement
                </button>
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

// Global variables for modal state
let currentYear = null;
let currentConference = null;

// Toggle admin panel
function toggleAdminPanel() {
    const toggle = document.getElementById('adminToggle');
    const panel = document.getElementById('adminPanel');

    toggle.classList.toggle('active');
    panel.classList.toggle('active');
}

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Add Year Modal
function openAddYearModal() {
    document.getElementById('newYear').value = new Date().getFullYear();
    openModal('addYearModal');
}

// Add Conference Modal
function openAddConferenceModal(year = null) {
    currentYear = year;
    const yearSelect = document.getElementById('conferenceYear');
    yearSelect.innerHTML = '';

    // Populate year dropdown
    placementsData.forEach(yearData => {
        const option = document.createElement('option');
        option.value = yearData.year;
        option.textContent = yearData.year;
        if (year && yearData.year === year) {
            option.selected = true;
        }
        yearSelect.appendChild(option);
    });

    openModal('addConferenceModal');
}

// Add Placement Modal
function openAddPlacementModal(year, conferenceName) {
    currentYear = year;
    currentConference = conferenceName;
    openModal('addPlacementModal');
}

// Form submissions
document.getElementById('addYearForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const year = parseInt(document.getElementById('newYear').value);

    // Check if year already exists
    if (placementsData.find(item => item.year === year)) {
        alert('This year already exists!');
        return;
    }

    // Add new year
    placementsData.push({
        year: year,
        conferences: []
    });

    // Sort by year (newest first)
    placementsData.sort((a, b) => b.year - a.year);

    // Update display
    filteredData = [...placementsData];
    populateFilters();
    renderPlacements();
    updateStats();

    closeModal('addYearModal');
    alert(`Year ${year} added successfully!`);
});

document.getElementById('addConferenceForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const year = parseInt(document.getElementById('conferenceYear').value);
    const name = document.getElementById('conferenceName').value;
    const location = document.getElementById('conferenceLocation').value;
    const date = document.getElementById('conferenceDate').value;

    // Find the year and add conference
    const yearData = placementsData.find(item => item.year === year);
    if (yearData) {
        yearData.conferences.push({
            name: name,
            location: location,
            date: date,
            placements: []
        });

        // Update display
        filteredData = [...placementsData];
        populateFilters();
        renderPlacements();
        updateStats();

        closeModal('addConferenceModal');
        alert('Conference added successfully!');

        let payload = {
            name: name,
            date: date,
            location: location,
            year: year
        }
        fetch("http://127.0.0.1:8000/achievements/add_conference/", {
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        })

        // Clear form
        document.getElementById('addConferenceForm').reset();
    }
});

document.getElementById('addPlacementForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const student = document.getElementById('placementStudent').value;
    const event = document.getElementById('placementCompany').value;
    const rank = document.getElementById('placementPosition').value;

    // Find the year and conference
    const yearData = placementsData.find(item => item.year == currentYear);
    if (yearData) {
        const conference = yearData.conferences.find(conf => conf.name === currentConference);
        if (conference) {
            conference.placements.push({
                students: student,
                event: event,
                rank: rank
            });

            // Update display
            filteredData = [...placementsData];
            populateFilters();
            renderPlacements();
            updateStats();

            closeModal('addPlacementModal');
            alert('Placement added successfully!');

            let payload = {
                conference: currentConference,
                eventName: event,
                students: student,
                year: currentYear,
                rank: rank
            }
            fetch("http://127.0.0.1:8000/achievements/add_achievement/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(payload)
            })

            // Clear form
            document.getElementById('addPlacementForm').reset();
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);