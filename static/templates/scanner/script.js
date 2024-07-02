import {getUrlParam} from "../../common/script.js";

let resultLog = document.getElementById("result-log");
let deviceIds = [];
let currentDeviceIndex = 0;

function forceRequestPermissions() {
  navigator.permissions.query({name: 'camera'})
    .then((permissionObj) => {
      console.log(permissionObj)
      if (permissionObj.state === "prompt") {
        setTimeout(forceRequestPermissions, 1000);
      } else if (permissionObj.state === "granted") {
        fetchDevices();
      }
    })
    .catch((error) => {
      console.log('Got error :', error);
    })
}

function fetchDevices() {
  navigator.mediaDevices
    .enumerateDevices()
    .then((devices) => {
      devices
        .filter((device) => device.kind === "videoinput")
        .forEach((device) => {
          deviceIds.push(device.deviceId)
        });
    })
    .catch((err) => {
      console.error(`${err.name}: ${err.message}`);
    });
}

function handleCameraChange() {
  const max_index = deviceIds.length - 1
  currentDeviceIndex += 1
  if (currentDeviceIndex > max_index) {
    currentDeviceIndex = 0
  }
  restartCameraStream()
}


function handleScan() {
  resultLog.innerText = "Processing..."

  function runDetection(nextDetections) {
    // Run single detection
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');

    // Run barcode detection on image data
    Quagga.decodeSingle({
      decoder: {
        readers: ['upc_reader', 'ean_reader', "ean_8_reader", "i2of5_reader", "2of5_reader", "code_39_reader", "code_128_reader"]
      },
      type: "ImageStream",
      inputStream: {
        size: canvas.width,
        singleChannel: false
      },
      locator: {
        patchSize: 'medium',
        halfSample: true
      },
      numOfWorkers: 0,
      locate: true,
      src: dataURL,
    }, result => {
      if (result && result.codeResult) {
        detections.push(result.codeResult.code)

      } else {
        detections.push(null)
      }
    });
    nextDetections = nextDetections--
    if (nextDetections === 0) {
      return handlePostDetections(detections)
    }
    setTimeout(() => {
      runDetection(nextDetections - 1)
    }, 30)
  }


  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  let detections = []

  runDetection(5)
}

function handlePostDetections(detections) {
  const itemCounts = {};
  const percentageMap = {};
  let notNullDetections = detections.filter((det) => det != null)
  if (notNullDetections.length === 0) {
    resultLog.innerText = "No detections"
    return
  }
  notNullDetections.forEach(item => {
    itemCounts[item] = (itemCounts[item] || 0) + 1;
  });
  const totalItems = notNullDetections.length;

  // Calculate the percentage for each item
  Object.keys(itemCounts).forEach(item => {
    const percentage = (itemCounts[item] / totalItems) * 100;
    percentageMap[item] = percentage.toFixed(2) + '%';
  });

  let maxPercentage = 0;
  let maxItem = null;

  Object.entries(percentageMap).forEach(([item, percentage]) => {
    const numericPercentage = parseFloat(percentage);
    if (numericPercentage >= 80 && numericPercentage > maxPercentage) {
      maxPercentage = numericPercentage;
      maxItem = item;
    }
  });

  if (maxItem == null) {
    resultLog.innerText = "Multiple possible detections, try again"
    return
  }
  resultLog.innerText = "Detected bar code: " + maxItem
  redirectWithBarcode(maxItem)

}

function redirectWithBarcode(bar_code) {
  const return_url = getUrlParam('return_url')
  if (return_url === null) return;
  window.location.href = `${return_url}?bar_code=${bar_code}`;

}

function restartCameraStream() {
  resultLog.innerText = ""
  resultLog.innerText = `Current camera id: ${deviceIds[currentDeviceIndex]} (${currentDeviceIndex})`
  navigator.mediaDevices.getUserMedia(
    {
      video: {
        deviceId: {
          exact: deviceIds[currentDeviceIndex],
        },
        width: {ideal: 1920},
        height: {ideal: 1080},
      },
    }
  )
    .then(function (stream) {
      const video = document.getElementById('video');
      video.srcObject = stream;
    })
    .catch(function (err) {
      console.error(err);
    });
}

function restartAutoCameraStream() {
  resultLog.innerText = "Current camera auto"
  navigator.mediaDevices.getUserMedia(
    {
      video: {
        facingMode: "environment",
        width: {ideal: 1920},
        height: {ideal: 1080},
      },
    }
  )
    .then(function (stream) {
      const video = document.getElementById('video');
      video.srcObject = stream;
    })
    .catch(function (err) {
      console.error(err);
    });
}

document.getElementById('scan-button').addEventListener('click', handleScan);
document.getElementById('camera-change-button').addEventListener('click', handleCameraChange);
document.getElementById('camera-auto-button').addEventListener('click', restartAutoCameraStream);

forceRequestPermissions()
restartAutoCameraStream()
