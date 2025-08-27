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
            <div class="event-name"><a href="/events/event/${event.id}">${event.name}</a></div>
            <div class="event-date">${event.team}</div>
        `;
        // <span class="event-status status-${event.type[0]}">
        //         ${event.type[1]}
        //     </span>
        //     <span class="event-status status-${event.cluster[0]}">
        //         ${event.cluster[1]}
        //     </span>
        
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
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        alert('New passwords do not match!');
        return;
    }

    if (newPassword.length < 6) {
        alert('Password must be at least 6 characters long!');
        return;
    }

    // Simulate password update
    alert('Password updated successfully!');
    closePasswordModal();
});

// Delete account confirmation
function confirmDelete() {
    const confirmed = confirm(
        'Are you sure you want to delete your account? This action cannot be undone.'
    );
    
    if (confirmed) {
        const doubleConfirm = confirm(
            'This will permanently delete all your data. Are you absolutely sure?'
        );
        
        if (doubleConfirm) {
            alert('Account deletion initiated. You will be redirected to the homepage.');
            // In a real app, this would make an API call to delete the account
            // window.location.href = '/';
        }
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