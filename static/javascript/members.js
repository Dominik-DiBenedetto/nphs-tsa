const members = document.querySelectorAll('.member')

function toggleMenu(index) {
    const menu = document.getElementById(`menu-${index}`);

    closeAllMenus()
    menu.classList.add("show");
}

function closeAllMenus() {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        menu.classList.remove("show");
    });
}

function search(e)
{
    const term = e.target.value.trim().toLowerCase();

    members.forEach(member => {
        if (term === "") {
            member.classList.remove("hide")
        } else {
            let name = member.querySelector(".member-name").textContent.toLowerCase();
            let n_num = member.querySelector(".member-id").textContent.toLowerCase();
            if (!name.includes(term) && !n_num.includes(term)) {
                if (!member.classList.contains("hide")) member.classList.add("hide")
            }
            else member.classList.remove("hide")
        }
    })
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

// Search connection
document.querySelector(".filter-search").addEventListener("input", search)
