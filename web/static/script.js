$(document).ready(function() {
    var video = document.querySelector("#video");
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var imageData;

    navigator.mediaDevices.getUserMedia({video: true})
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.log("Error accessing webcam: ", error);
        });

    function predict() {
        // Taking the current frame from the video
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        imageData = canvas.toDataURL('image/jpeg');

        // Sending the image data to the Flask server
        $.ajax({
            url: '/prediction/predict',
            type: 'POST',
            data: {
                imageData: imageData
            },
            success: function(response) {
                // Displaying the prediction result on the web page
                var prediction = response.prediction;
                $('#prediction').text('Prediction: ' + prediction);
            },
            error: function(error) {
                console.log("Error predicting: ", error);
            }
        });

        // Repeating the predict function every 1 second
        setTimeout(predict, 1000);
    }

    // Starting the prediction automatically after the page loads
    predict();
});
