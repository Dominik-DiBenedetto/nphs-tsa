let teamCount = 0;
let eventData = {
    name: "",
    description: "",
    prompt: "",
    cegFile: null,
    teams: [],
};

// Initialize the page
function init() {
    setupEventListeners();
    addTeam(); // Add first team by default
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document
        .getElementById("eventForm")
        .addEventListener("submit", handleSubmit);

    // File upload
    document
        .getElementById("cegFile")
        .addEventListener("change", handleFileUpload);

    // Real-time form updates
    document
        .getElementById("eventName")
        .addEventListener("input", updateEventData);
    document
        .getElementById("eventDescription")
        .addEventListener("input", updateEventData);
    document
        .getElementById("eventPrompt")
        .addEventListener("input", updateEventData);
}

// Add new team
function addTeam() {
    teamCount++;
    const teamsContainer = document.getElementById("teamsContainer");

    const teamCard = document.createElement("div");
    teamCard.className = "team-card slide-in";
    teamCard.id = `team-${teamCount}`;

    teamCard.innerHTML = `
                <div class="team-header">
                    <div class="team-title">Team ${teamCount}</div>
                    <div class="team-controls">
                        <button type="button" class="btn btn-secondary" onclick="toggleTeamMembers(${teamCount})">
                            <span id="toggle-icon-${teamCount}"></span> Toggle Members
                        </button>
                        <button type="button" class="btn btn-danger" onclick="removeTeam(${teamCount})">
                            Remove
                        </button>
                    </div>
                </div>
                <div class="members-grid" id="members-${teamCount}">
                    ${generateMemberInputs(teamCount)}
                </div>
            `;

    teamsContainer.appendChild(teamCard);

    // Add team to eventData
    eventData.teams.push({
        id: teamCount,
        members: ["", "", "", "", "", ""],
    });
}

// Generate member input fields
function generateMemberInputs(teamId) {
    let inputs = "";
    for (let i = 1; i <= 6; i++) {
        inputs += `
                    <div class="member-input">
                        <div class="member-number">${i}</div>
                        <input type="text" 
                               id="team-${teamId}-member-${i}" 
                               name="team-${teamId}-member-${i}" 
                               class="form-input" 
                               placeholder="Member ${i} name..."
                               onchange="updateTeamMember(${teamId}, ${i}, this.value)">
                    </div>
                `;
    }
    return inputs;
}

// Remove team
function removeTeam(teamId) {
    if (teamCount <= 1) {
        alert("You must have at least one team!");
        return;
    }

    const teamCard = document.getElementById(`team-${teamId}`);
    if (teamCard) {
        teamCard.style.animation = "fadeOut 0.3s ease forwards";
        setTimeout(() => {
            teamCard.remove();
            // Remove from eventData
            eventData.teams = eventData.teams.filter(
                (team) => team.id !== teamId
            );
        }, 300);
    }
}

// Toggle team members visibility
function toggleTeamMembers(teamId) {
    const membersGrid = document.getElementById(`members-${teamId}`);

    if (membersGrid.style.display === "none") {
        membersGrid.style.display = "grid";
    } else {
        membersGrid.style.display = "none";
    }
}

// Update team member
function updateTeamMember(teamId, memberIndex, value) {
    const team = eventData.teams.find((t) => t.id === teamId);
    if (team) {
        team.members[memberIndex - 1] = value;
    }
}

// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    const fileUpload = document.getElementById("cegUpload");
    const fileInfo = document.getElementById("fileInfo");

    if (file) {
        fileUpload.classList.add("has-file");
        fileInfo.innerHTML = `
                    <strong>Selected file:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${(file.size / 1024 / 1024).toFixed(
                        2
                    )} MB<br>
                    <strong>Type:</strong> ${file.type || "Unknown"}
                `;
        eventData.cegFile = file;
    } else {
        fileUpload.classList.remove("has-file");
        fileInfo.innerHTML = "";
        eventData.cegFile = null;
    }
}

// Update event data
function updateEventData() {
    eventData.name = document.getElementById("eventName").value;
    eventData.description = document.getElementById("eventDescription").value;
    eventData.prompt = document.getElementById("eventPrompt").value;
}

// Handle form submission
function handleSubmit(event) {
    event.preventDefault();

    // Validate required fields
    if (!eventData.name.trim()) {
        alert("Please enter an event name!");
        document.getElementById("eventName").focus();
        return;
    }

    if (!eventData.description.trim()) {
        alert("Please enter an event description!");
        document.getElementById("eventDescription").focus();
        return;
    }

    // Disable submit button
    const submitBtn = document.getElementById("submitBtn");
    submitBtn.disabled = true;
    submitBtn.innerHTML = "Creating Event...";

    // Create event
    console.log(eventData.cegFile)
    let formData = new FormData();
    formData.append('Name', eventData.name.trim());
    formData.append('Description', eventData.description.trim());
    formData.append('Prompt', eventData.prompt.trim());
    formData.append('CEG', eventData.cegFile); // File input
    formData.append('Teams', JSON.stringify(eventData.teams));

    fetch("/events/add_event/", {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

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

// Add CSS for fadeOut animation
const style = document.createElement("style");
style.textContent = `
            @keyframes fadeOut {
                to {
                    opacity: 0;
                    transform: translateX(-100%);
                }
            }
        `;
document.head.appendChild(style);

// Initialize when page loads
document.addEventListener("DOMContentLoaded", init);
