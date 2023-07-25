// Declare the Chart objects outside the $(document).ready() function
let distanceChart, hujanChart, flowChart;

$(document).ready(function () {
  // Chart.js initialization
  const distanceCtx = document.getElementById("distanceChart").getContext("2d");
  const hujanCtx = document.getElementById("hujanChart").getContext("2d");
  const flowCtx = document.getElementById("flowChart").getContext("2d");

  distanceChart = new Chart(distanceCtx, {
    type: "line",
    data: {
      datasets: [{ label: "Distance", borderColor: 'rgba(255, 99, 132, 1)', data: [] }],
    },
    options: {
      borderWidth: 3,
    },
  });

  hujanChart = new Chart(hujanCtx, {
    type: "line",
    data: {
      datasets: [{ label: "Hujan", borderColor: 'rgba(75, 192, 192, 1)', data: [] }],
    },
    options: {
      borderWidth: 3,
    },
  });

  flowChart = new Chart(flowCtx, {
    type: "line",
    data: {
      datasets: [{ label: "Flow", borderColor: 'rgba(54, 162, 235, 1)', data: [] }],
    },
    options: {
      borderWidth: 3,
    },
  });

  function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    chart.update();
  }

  function removeFirstData(chart) {
    chart.data.labels.splice(0, 1);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  // SocketIO event handler
  var socket = io.connect();

  socket.on("updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.distance + " :: " + msg.flow + " :: " + msg.hujan);

    // Show only MAX_DATA_COUNT data
    if (distanceChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(distanceChart);
    }
    addData(distanceChart, msg.date, msg.distance);

    if (hujanChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(hujanChart);
    }
    addData(hujanChart, msg.date, msg.hujan);

    if (flowChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(flowChart);
    }
    addData(flowChart, msg.date, msg.flow);
  });
});
