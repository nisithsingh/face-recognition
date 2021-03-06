    var person;
    var timer = 0;
    var imgCount = 1;
    
    window.addEventListener("DOMContentLoaded", function () {
    // Grab elements, create settings, etc.
   
     var   video = document.getElementById("video"),
        videoObj = { "video": true },
        errBack = function (error) {
            console.log("Video capture error: ", error.code);
        };
 
    if (navigator.getUserMedia) { // Standard
        navigator.getUserMedia(videoObj, function (stream) {
            video.src = stream;
            video.play();
        }, errBack);
    } else if (navigator.webkitGetUserMedia) { // WebKit-prefixed
        navigator.webkitGetUserMedia(videoObj, function (stream) {
            video.src = window.webkitURL.createObjectURL(stream);
            video.play();
        }, errBack);
    }
 
    // Trigger photo take
    document.getElementById("snap").addEventListener("click", function () {
        if (person == null) {
          person = prompt("Please enter your name");
        }
        timer = setInterval(function(){UploadToServer()},1000);
        
    });
}, false);


function UploadToServer() {

    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, 600, 400);

    var img = canvas.toDataURL('image/jpeg', 0.9).split(',')[1];


    $.ajax({
        url: "/save/",
        type: "POST",
        data: "{ 'person': '" + person +"','image': '" + img + "' }",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function () {
            //alert('Image Uploaded!!');
            $("#snap").removeAttr('disabled');
            $("#snap").attr("value", "Uploaded image " + imgCount + " of 10" );
            // $("#snap").attr("value", "Upload");
        },
        error: function (e) {
            alert("Error : " + e);
            $("#snap").removeAttr('disabled');
            $("#snap").attr("value", "Upload");
        }
    });

    if(imgCount == 10) {
        clearInterval(timer);
        alert("Please click on Compare tab to see if it recognizes you now...!!!")
      } else {
        imgCount++;
      }
    }