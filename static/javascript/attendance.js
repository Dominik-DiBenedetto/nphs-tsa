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

const deleteButtons = document.querySelectorAll(".delete")
deleteButtons.forEach(button => {
    button.addEventListener("click", (e) => {
        e.preventDefault()
        let n_num = button.getAttribute("data-nnum")
        let modal = document.querySelector(`.modal-${n_num}`)
        if (modal) {
            let active_modal = document.querySelector(".modal.active")
            if (active_modal) {
                active_modal.classList.remove("active")
            }
            modal.classList.add("active")
        }
    })
})

document.querySelectorAll(".cancel-delete-button").forEach(cancelBtn => {
    cancelBtn.addEventListener("click", (e) => {
        e.preventDefault()
        cancelBtn.parentElement.parentElement.classList.remove("active")
    })
})

document.querySelectorAll(".export-nnums").forEach(exportBtn => {
    let dateHolder = document.querySelector(`#${exportBtn.getAttribute("id").replace("export-", "")}`)
    let members_holder = dateHolder.querySelector("table").querySelector(".membersTableBody")
    
    exportBtn.addEventListener("click", (e) => {
        e.preventDefault()
        
        let fileText = ""
        Array.from(members_holder.children).forEach(member => {
            let member_data = member.querySelector("tr")
            let name = member.querySelector(".member-name")
            let nnum = member.querySelector(".member-id")
            fileText += `${name.innerText} - ${nnum.innerText}\n`
        })
        saveTextToFile(fileText, `${exportBtn.getAttribute("id").replace("export-date-", "")}-members`)
    })
})

function saveTextToFile(textToSave, filename) {
    // Create a Blob object from the text content
    const blob = new Blob([textToSave], { type: 'text/plain;charset=utf-8' });
  
    // Create a URL for the Blob
    const url = URL.createObjectURL(blob);
  
    // Create a temporary anchor element
    const a = document.createElement('a');
    a.href = url;
    a.download = filename; // Set the desired filename for the download
  
    // Programmatically click the anchor to trigger the download
    document.body.appendChild(a); // Append to body is good practice for compatibility
    a.click();
    document.body.removeChild(a); // Clean up the temporary element
  
    // Revoke the object URL to free up resources
    URL.revokeObjectURL(url);
  }