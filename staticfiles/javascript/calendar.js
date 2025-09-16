let events = [];
        let currentDate = new Date();
        let selectedDate = null;

        // Load events from localStorage with proper error handling
        function loadEvents() {
            try {
                const savedEvents = localStorage.getItem('calendarEvents');
                if (savedEvents) {
                    const parsed = JSON.parse(savedEvents);
                    events = Array.isArray(parsed) ? parsed : [];
                } else {
                    // Initialize with sample events
                    events = [

                    ];
                    saveEvents();
                }
                console.log('Events loaded:', events.length, 'events');
            } catch (error) {
                console.error('Error loading events:', error);
                events = [];
            }
        }

        function saveEvents() {
            try {
                localStorage.setItem('calendarEvents', JSON.stringify(events));
                console.log('Events saved:', events.length, 'events');
            } catch (error) {
                console.error('Error saving events:', error);
            }
        }

        function renderCalendar() {
            console.log('Rendering calendar...');
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();
            
            // Update month display
            const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
            document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;
            
            // Clear calendar grid
            const calendarGrid = document.getElementById('calendarGrid');
            calendarGrid.innerHTML = '';
            
            // Add day headers
            const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            dayHeaders.forEach(day => {
                const dayHeader = document.createElement('div');
                dayHeader.className = 'day-header';
                dayHeader.textContent = day;
                calendarGrid.appendChild(dayHeader);
            });
            
            // Get first day of month and number of days
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const startDate = new Date(firstDay);
            startDate.setDate(startDate.getDate() - firstDay.getDay());
            
            const calendarDays = [];
            
            // Generate calendar days
            for (let i = 0; i < 42; i++) {
                const date = new Date(startDate);
                date.setDate(startDate.getDate() + i);
                
                const dayElement = document.createElement('div');
                dayElement.className = 'calendar-day';
                dayElement.dataset.date = date.toISOString().split('T')[0];
                
                if (date.getMonth() !== month) {
                    dayElement.classList.add('other-month');
                }
                
                if (date.toDateString() === new Date().toDateString()) {
                    dayElement.classList.add('today');
                }
                
                const dayNumber = document.createElement('div');
                dayNumber.className = 'day-number';
                dayNumber.textContent = date.getDate();
                dayElement.appendChild(dayNumber);
                
                if (Array.isArray(events)) {
                    const dayEvents = events.filter(event => {
                        const eventStart = new Date(`${event.startDate}T00:00:00`);
                        const eventEnd = new Date(event.endDate ? `${event.endDate}T00:00:00` : `${event.startDate}T00:00:00`);
                        const currentDay = new Date(date);
                        
                        // Reset time to compare dates only
                        currentDay.setHours(0, 0, 0, 0);
                        
                        // Only show single-day events as individual items
                        return currentDay >= eventStart && currentDay <= eventEnd && event.startDate === (event.endDate || event.startDate);
                    });
                    
                    dayEvents.forEach(event => {
                        const eventElement = document.createElement('div');
                        eventElement.className = `event-item event-${event.category}`;
                        eventElement.textContent = event.title;
                        dayElement.appendChild(eventElement);
                    });
                }
                
                dayElement.addEventListener('click', () => openDayModal(date));
                calendarGrid.appendChild(dayElement);
                calendarDays.push({ element: dayElement, date: new Date(date) });
            }
            
            renderSpanningEvents(calendarDays);
            
            console.log('Calendar rendered successfully');
        }

        function renderSpanningEvents(calendarDays) {
            if (!Array.isArray(events)) return;
            
            // Get multi-day events
            const multiDayEvents = events.filter(event => 
                event.startDate !== (event.endDate || event.startDate)
            );
            
            multiDayEvents.forEach((event, eventIndex) => {
                const eventStart = new Date(`${event.startDate}T00:00:00`);
                const eventEnd = new Date(`${event.endDate}T00:00:00`);
                
                // Find start and end positions in the calendar grid
                let startIndex = -1;
                let endIndex = -1;
                
                calendarDays.forEach((day, index) => {
                    const dayDate = new Date(day.date);
                    dayDate.setHours(0, 0, 0, 0);
                    
                    if (dayDate.getTime() === eventStart.getTime()) {
                        startIndex = index;
                    }
                    if (dayDate.getTime() === eventEnd.getTime()) {
                        endIndex = index;
                    }
                });
                
                if (startIndex === -1 || endIndex === -1) return;
                
                // Calculate which week rows the event spans
                const startRow = Math.floor(startIndex / 7);
                const endRow = Math.floor(endIndex / 7);
                
                // Create spanning events for each row
                for (let row = startRow; row <= endRow; row++) {
                    const rowStartIndex = row * 7;
                    const rowEndIndex = Math.min(rowStartIndex + 6, 41);
                    
                    const segmentStart = Math.max(startIndex, rowStartIndex);
                    const segmentEnd = Math.min(endIndex, rowEndIndex);
                    
                    if (segmentStart <= segmentEnd) {
                        createSpanningEventElement(
                            calendarDays[segmentStart].element,
                            segmentEnd - segmentStart + 1,
                            event,
                        );
                    }
                }
            });
        }
        
        function createSpanningEventElement(startDayElement, spanDays, event) {
            const spanningEvent = document.createElement('div');
            spanningEvent.className = `spanning-event event-${event.category}`;
            spanningEvent.textContent = event.title;
            
            // Position the spanning event
            const topOffset = 30 + (startDayElement.children.length % 3) * 25; // Stack multiple events
            spanningEvent.style.top = `${topOffset}px`;
            spanningEvent.style.left = '2px';
            spanningEvent.style.right = '2px';
            
            // Calculate width based on number of days to span
            const dayWidth = 100 / 7; // Each day is 1/7 of the week
            spanningEvent.style.width = `calc(${spanDays * dayWidth}vw - 26px)`;
            
            // Add click handler
            spanningEvent.addEventListener('click', (e) => {
                e.stopPropagation();
                // Find the date of the clicked spanning event
                const eventDate = new Date(`${event.startDate}T00:00:00`);
                openDayModal(eventDate);
            });
            
            startDayElement.appendChild(spanningEvent);
        }

        function changeMonth(direction) {
            let newMonth = currentDate.getMonth()+direction
            currentDate.setDate(1)
            currentDate.setMonth(newMonth);
            console.log(currentDate.getMonth(), newMonth)
            renderCalendar();
        }

        function openDayModal(date) {
            selectedDate = date;
            const modalTitle = document.getElementById('modalTitle');
            modalTitle.textContent = date.toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            
            displayDayEvents(date);
            document.getElementById('dayModal').style.display = 'block';
        }

        function closeDayModal() {
            const modal = document.getElementById('dayModal')
            hideAddEventForm();
        }

        function displayDayEvents(date) {
            const eventList = document.getElementById('eventList');
            eventList.innerHTML = '';
            
            if (!Array.isArray(events)) {
                events = [];
                return;
            }
            
            const dayEvents = events.filter(event => {
                const eventStart = new Date(`${event.startDate}T00:00:00`);
                const eventEnd = new Date(event.endDate ? `${event.endDate}T00:00:00` : `${event.startDate}T00:00:00`);
                const currentDay = new Date(date);
                
                // Reset time to compare dates only
                currentDay.setHours(0, 0, 0, 0);
                
                return currentDay >= eventStart && currentDay <= eventEnd;
            });
            
            if (dayEvents.length === 0) {
                eventList.innerHTML = '<p style="color: #6b7280; text-align: center; padding: 20px;">No events for this day</p>';
                return;
            }
            
            dayEvents.forEach(event => {
                const eventDetail = document.createElement('div');
                eventDetail.className = 'event-detail';
                eventDetail.style.borderLeftColor = getCategoryColor(event.category);
                
                eventDetail.innerHTML = `
                    <h4>${event.title}</h4>
                    <p><strong>Category:</strong> ${event.category.charAt(0).toUpperCase() + event.category.slice(1)}</p>
                    ${event.description ? `<p><strong>Description:</strong> ${event.description}</p>` : ''}
                    <p><strong>Date:</strong> ${event.startDate}${event.endDate && event.endDate !== event.startDate ? ` to ${event.endDate}` : ''}</p>
                    <div class="event-actions">
                        ${event.link ? `<a href="${event.link}" target="_blank" class="btn btn-primary">View Event</a>` : ''}
                        <button class="btn btn-danger" onclick="deleteEvent(${event.id})">Delete</button>
                    </div>
                `;
                
                eventList.appendChild(eventDetail);
            });
        }

        function getCategoryColor(category) {
            const colors = {
                meeting: '#3b82f6',
                deadline: '#ef4444',
                fundraiser: '#10b981',
                conference: '#f59e0b',
                other: '#8b5cf6'
            };
            return colors[category] || colors.other;
        }

        function showAddEventForm() {
            const form = document.getElementById('addEventForm');
            if (form == null) return;

            form.style.display = 'block';
            
            // Set default date to selected date
            const dateStr = selectedDate.toISOString().split('T')[0];
            document.getElementById('eventStartDate').value = dateStr;
        }

        function hideAddEventForm() {
            let form = document.getElementById('addEventForm')
            if (form == null) return;

            form.style.display = 'none';
            form.querySelector('form').reset();
        }

        function addEvent(e) {
            e.preventDefault();
            console.log('Adding event...');
            
            if (document.getElementById('eventTitle') == null) return;
            const title = document.getElementById('eventTitle').value;
            const description = document.getElementById('eventDescription').value;
            const category = document.getElementById('eventCategory').value;
            const startDate = document.getElementById('eventStartDate').value;
            const endDate = document.getElementById('eventEndDate').value || startDate;
            // const link = document.getElementById('eventLink').value;
            
            const newEvent = {
                id: Date.now(),
                title,
                description,
                category,
                startDate,
                endDate,
                link: "", //link
            };
            
            console.log('New event:', newEvent);
            
            events.push(newEvent);
            saveEvents();
            
            renderCalendar();
            displayDayEvents(selectedDate);
            hideAddEventForm();
            
            console.log('Event added successfully');
        }

        function deleteEvent(eventId) {
            if (confirm('Are you sure you want to delete this event?')) {
                console.log('Deleting event:', eventId);
                events = events.filter(event => event.id !== eventId);
                saveEvents();
                renderCalendar();
                displayDayEvents(selectedDate);
                console.log('Event deleted successfully');
            }
        }

        // Initialize calendar
        console.log('Initializing calendar...');
        loadEvents();
        renderCalendar();

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('dayModal');
            if (event.target === modal) {
                closeDayModal();
            }
        }