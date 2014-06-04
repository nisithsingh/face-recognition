var webcam = (function(){

    var video = document.getElementById("live_video"),
        canvas = document.getElementById('canvas');

    function play() {
        if (navigator.getUserMedia) {
            navigator.getUserMedia({video: true, audio: true, 
              toString : function() {return "video,audio";} }, onSuccess, onError);
        } else {
            changeStatus('getUserMedia is not supported in this browser.', true);
        }
    }

    function onSuccess(stream) {
        var source;
         if (window.webkitURL) {
            source = window.webkitURL.createObjectURL(stream);
        } else {
            source = stream; // Opera and Firefox
        }
 
        video.autoplay = true;
        video.src = source;
        changeStatus('Connected.', false);
    }

    function onError() {
        changeStatus('Please accept the getUserMedia permissions! Refresh to try again.', true);
    }

    function changeStatus(msg, error) {
        var status = document.getElementById('status');
        status.innerHTML = msg;
        status.style.color = (error) ? 'red' : 'green';
    }


    // allow the user to take a screenshot
    function setupPhotoBooth() {
        var takeButton = document.getElementById("Submit");
        takeButton.addEventListener('click', takePhoto, true);
        

        // var saveButton = document.createElement('button');
        // saveButton.id = 'save';
        // saveButton.innerText = 'Save!';
        // saveButton.disabled = true;
        // saveButton.addEventListener('click', savePhoto, true);
        // document.body.appendChild(saveButton);

    }

    function takePhoto() {

        // set our canvas to the same size as our video
        canvas.width = video.width;
        canvas.height = video.height;

        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // allow us to save
        // var saveButton = document.getElementById('save');
        // saveButton.disabled = false;

    }

    function savePhoto() {
        var data = canvas.toDataURL("image/png");
        data = data.replace("image/png","image/octet-stream");
        document.location.href = data;

    }

    return {
        init: function() {
            changeStatus('Please accept the permissions dialog.', true);
            video.width = 640;
            video.height = 480;
            document.body.appendChild(video);
            document.body.appendChild(canvas);
            navigator.getUserMedia || (navigator.getUserMedia = navigator.mozGetUserMedia || navigator.webkitGetUserMedia || navigator.msGetUserMedia);
            play();
            setupPhotoBooth();
        }()

    }

})();