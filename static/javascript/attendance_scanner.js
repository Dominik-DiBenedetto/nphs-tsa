const VIEW = document.querySelector(".scanner-view")

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

function saveRecordToLocalStorage(nNumber, formattedDate) {
    const recordBody = {
        n_num: nNumber,
        date: formattedDate
    };

    let currentStorage = JSON.parse(localStorage.getItem('pending_records')) || [];
    currentStorage.push(recordBody);
    localStorage.setItem('pending_records', JSON.stringify(currentStorage));
}

let lastScannedNumber = ""
function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    if (decodedText) {
        let nNumber = decodedText
        if (!decodedText.includes("N")) {
            let nNumberNum = parseInt(nNumber, 10)
            if (isNaN(nNumberNum)) {
                return
            }
            nNumber = "N" + nNumberNum
        }

        if (lastScannedNumber === nNumber) return;
        lastScannedNumber = nNumber

        const today = new Date();
        const formattedDate = today.toISOString().slice(0, 10);
        saveRecordToLocalStorage(nNumber, formattedDate)

        alert("scanned " + nNumber)
        setTimeout(() => {
            if (lastScannedNumber === nNumber) lastScannedNumber = "";
        }, 3000)
    }
}

function onScanFailure(error) {

}

let html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", {
        fps: 10, qrbox: (viewfinderWidth, viewfinderHeight) => {
            // Calculate dynamic dimensions, e.g., 70% of the smaller dimension
            let minDimension = Math.min(viewfinderWidth, viewfinderHeight);
            let qrboxSize = minDimension * 0.7; // Adjust as needed
            return { width: qrboxSize, height: qrboxSize, disableFlip: false, focusMode: "continuous" };
        }
}, /* verbose= */ false);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);

function sendPendingScans() {
    const data = localStorage.getItem("pending_records")
    if (!data || data === "[]") return;

    const blob = new Blob([data], { type: "application/json" })
    navigator.sendBeacon("/members/attendance/scan/", blob)
}

async function verifyStoredScans() {
    const backupData = localStorage.getItem('pending_records')
    if (!backupData || backupData === "[]") return

    try {
        const response = await fetch("/members/attendance/confirm_scan", {
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: backupData
        })
        if (response.ok) {
            localStorage.removeItem("pending_records")
            console.log("Successfully cleared stored scans!")
        }
    } catch (error) {
        console.error("Sync failed, keeping data for next attempt.")
    }
}

document.addEventListener('visibilitychange', async () => {
    if (document.visibilityState === "hidden") sendPendingScans();
    else verifyStoredScans()
})
document.addEventListener('DOMContentLoaded', verifyStoredScans)