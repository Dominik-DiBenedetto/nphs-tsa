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

Quagga.init({
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#interactive'),
        constraints: {
            // Critical for iPhone: Standard resolution works best
            width: 640,
            height: 480,
            facingMode: "environment" // Uses back camera
        },
    },
    decoder: {
        // Only enable what you need to improve speed
        readers: ["code_128_reader", "ean_reader"]
    }
}, function(err) {
    if (err) {
        console.error(err);
        return;
    }
    Quagga.start();
});

let lastScannedNumber = ""

Quagga.onDetected((data) => {
    if (data.codeResult.code) {
        let nNumber = data.codeResult.code;
        if (!data.codeResult.code.includes("N")) {
            try {
                nNumberNum = parseInt(nNumber)
            } catch (error) {
                return
            }
            nNumber = "N" + toString(nNumberNum)
        }
        if (lastScannedNumber === nNumber) return;

        lastScannedNumber = nNumber

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
        alert("scanned3!")
        setTimeout(() => {
            if (lastScannedNumber === nNumber) lastScannedNumber = "";
        }, 5000)
    }
});