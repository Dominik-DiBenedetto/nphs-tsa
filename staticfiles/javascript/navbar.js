
// Auto-hide navbar on scroll
let lastScrollY = window.scrollY;
const navbar = document.getElementById('navbar');

function handleScroll() {
    const currentScrollY = window.scrollY;

    if (currentScrollY < lastScrollY || currentScrollY < 10) {
        // Scrolling up or near top
        navbar.classList.remove('hidden');
    } else {
        // Scrolling down
        navbar.classList.add('hidden');
    }

    lastScrollY = currentScrollY;
}

// Throttle scroll events for better performance
let ticking = false;
function throttledScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            handleScroll();
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', throttledScroll);

// Sidebar toggle functionality
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

function toggleSidebar() {
    sidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('active');
    document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
}

function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

sidebarToggle.addEventListener('click', toggleSidebar);
sidebarOverlay.addEventListener('click', closeSidebar);

// Close sidebar on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
        closeSidebar();
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        closeSidebar();
    }
});

// Active link handling
const active_nav_link = document.querySelector("[data-active-navbar-link]")
const active_sidebar_link = document.querySelector("[data-active-sidebar-link]")

const navbar_link_text = active_nav_link.getAttribute("data-active-navbar-link")
const sidebar_link_text = active_sidebar_link.getAttribute("data-active-sidebar-link")
if (navbar_link_text != "none") {
    Array.from(active_nav_link.querySelectorAll("a")).find(el => el.innerText === navbar_link_text).classList.add("active");
} else {
    Array.from(active_sidebar_link.querySelectorAll("a")).find(el => el.innerText == sidebar_link_text).classList.add("active");
}