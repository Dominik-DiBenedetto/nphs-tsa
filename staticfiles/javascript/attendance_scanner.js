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

function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    if (decodedText && decodedText.includes("N")) {
        let nNumber = decodedText
        const today = new Date();
        const formattedDate = today.toISOString().slice(0, 10);
        fetch("/members/attendance/add", {
            method: "POST",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                n_num: nNumber,
                date: formattedDate
            })
        })
        alert("scanned2!")
    }
  }

  function onScanFailure(error) {

  }

  let html5QrcodeScanner = new Html5QrcodeScanner(
      "reader", { fps: 10, qrbox: (viewfinderWidth, viewfinderHeight) => {
        // Calculate dynamic dimensions, e.g., 70% of the smaller dimension
        let minDimension = Math.min(viewfinderWidth, viewfinderHeight);
        let qrboxSize = minDimension * 0.7; // Adjust as needed
        return { width: qrboxSize, height: qrboxSize, disableFlip: false, focusMode: "continuous" };
      } }, /* verbose= */ false);
  html5QrcodeScanner.render(onScanSuccess, onScanFailure);