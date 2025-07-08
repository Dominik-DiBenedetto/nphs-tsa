const CONTAINER = document.querySelector(".container")
const DATES = document.querySelectorAll(".date")

let dates = []
DATES.forEach((elm) => {
    let date = new Date(elm.textContent)
    dates.push(date)
})

function reorderDates() {
    dates.forEach((date) => {
        let dateStr = date.toISOString().split('T')[0];
        let dateDiv = document.querySelector(`#date-${dateStr}`)
        CONTAINER.appendChild(dateDiv)
    })
}

function sortDatesOldToNew(filteredDates){
    const sortedDates = filteredDates.sort((a, b) => {
        const dateA = new Date(a)
        const dateB = new Date(b)
        return dateA - dateB
    })
    return sortedDates
}

function sortDatesNewToOld(filteredDates){
    const sortedDates = filteredDates.sort((a, b) => {
        const dateA = new Date(a)
        const dateB = new Date(b)
        return dateB - dateA 
    })
    return sortedDates
}

const reorderDatesSelection = document.querySelector(".dateOrderFilter")
reorderDatesSelection.addEventListener('change', (e) => {
    const selected = e.target.value;
    if (selected === "ascending"){
        dates = sortDatesNewToOld(dates)
        reorderDates(dates)
    } else {
        dates = sortDatesOldToNew(dates)
        reorderDates(dates)
    }
})

dates = sortDatesNewToOld(dates)
reorderDates(dates)

const dateSelector = document.querySelector("#dateFilter")
dateSelector.addEventListener('change', (e) => {
    const selectedDate = e.target.value;
    console.log(selectedDate)
    if (document.querySelector(`#date-${selectedDate}`)) {
        DATES.forEach((date) => {
            let dateDiv = date.parentElement.parentElement.parentElement.parentElement
            if (dateDiv.id !== `date-${selectedDate}`) {
                dateDiv.classList.add("hidden-date")
            } else {
                dateDiv.classList.remove("hidden-date")
            };
        })
    } else {
        DATES.forEach((date) => {
            let dateDiv = date.parentElement.parentElement.parentElement.parentElement
            dateDiv.classList.remove("hidden-date")
        })
    }
    searchElms(search.value)
})

const search = document.querySelector("#searchInput")
const names = document.querySelectorAll(".member-name")
const ids = document.querySelectorAll(".member-id")

function searchElms(text) {
    let results = []
    names.forEach((nameElm) => {
        if (nameElm.textContent.toLowerCase().includes(text)) results.push(nameElm.parentElement.parentElement.parentElement.parentElement)
    })
    ids.forEach((idElm) => {
        if (idElm.textContent.toLowerCase().includes(text)) results.push(idElm.parentElement.parentElement.parentElement.parentElement)
    })
    DATES.forEach((date) => {
        let dateDiv = date.parentElement.parentElement.parentElement.parentElement
        if (results.includes(dateDiv)) {
            dateDiv.classList.remove("hidden-date-search")
        } else {
            if (!dateDiv.classList.contains("hidden-date-search")) dateDiv.classList.add("hidden-date-search")
        }
    })
}
search.addEventListener('keyup', (e) => {
    searchElms(e.target.value.toLowerCase())
})

function clearAllFilters() {
    search.value = ""
    dateSelector.value = null
    reorderDatesSelection.value = "ascending"
    DATES.forEach((date) => {
        let dateDiv = date.parentElement.parentElement.parentElement.parentElement
        if (dateDiv.classList.contains("hidden-date")) dateDiv.classList.remove("hidden-date")
        if (dateDiv.classList.contains("hidden-date-search")) dateDiv.classList.remove("hidden-date-search")
    })
}