function toggleMenu(index) {
    const menu = document.getElementById(`menu-${index}`);
    const isOpen = menu.classList.contains("show");

    // Close all other menus
    document.querySelectorAll(".dropdown-menu").forEach((m) => {
        m.classList.remove("show");
    });

    // Toggle current menu
    if (!isOpen) {
        menu.classList.add("show");
    }
}

function closeAllMenus() {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        menu.classList.remove("show");
    });
}

// Close menus when clicking outside
document.addEventListener("click", function (event) {
    if (!event.target.closest(".menu-container")) {
        closeAllMenus();
    }
});

// Close menus on escape key
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeAllMenus();
    }
});