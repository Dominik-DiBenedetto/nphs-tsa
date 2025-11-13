const eventData = JSON.parse(document.getElementById('events-data').textContent)

// Initialize page
function initializePage() {
    // Set avatar initials
    const initials = document.getElementById('userName').textContent.split(' ').map(n => n[0]).join('');
    document.getElementById('avatar').textContent = initials;

    // Populate events
    populateEvents();
}

// Populate events list
function populateEvents() {
    const eventsList = document.getElementById('eventsList');
    eventsList.innerHTML = '';

    eventData.forEach(event => {
        const eventItem = document.createElement('li');
        eventItem.className = 'event-item';
        
        eventItem.innerHTML = `
            <div class="event-name">${event.name}</div>
            <div class="event-date">${event.team}</div>
        `;
        // <span class="event-status status-${event.type[0]}">
        //         ${event.type[1]}
        //     </span>
        //     <span class="event-status status-${event.cluster[0]}">
        //         ${event.cluster[1]}
        //     </span>

        eventItem.addEventListener("click", (e) => {
            e.preventDefault();
            window.location.href = `/events/event/${event.id}#teams`
        })
        
        eventsList.appendChild(eventItem);
    });
}

// Password modal functions
function openPasswordModal() {
    document.getElementById('passwordModal').style.display = 'block';
}

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
    document.getElementById('passwordForm').reset();
}

// Handle password form submission
document.getElementById('passwordForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const newPassword = document.getElementById('newPassword').value;

    fetch("/members/update/", {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            viewing_nnum: document.querySelector("#userNnum").textContent,
            n_num: document.querySelector("#newNnum").value,
            name: document.querySelector("#newName").value,
            password: newPassword,
        }),
    })
    window.location.href = `/members/${document.querySelector("#newNnum").value}`
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

// Delete account confirmation
function confirmDelete() {
    const confirmed = confirm(
        'Are you sure you want to delete your account? This action cannot be undone.'
    );
    
    if (confirmed) {
        fetch("/members/delete/", {
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                n_num: document.querySelector("#userNnum").textContent,
                })
            })
    }
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('passwordModal');
    if (e.target === modal) {
        closePasswordModal();
    }
});

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage);