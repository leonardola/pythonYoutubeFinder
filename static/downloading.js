var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('download status changed', function(msg){

    var videoElement = $("#Downloading .downloading_video[video_id='"+msg.videoId+"']");
    var downloadData =  msg['downloadData'];
    var transferedPercentage = downloadData['_percent_str'].replace('%','').trim();

    videoElement.find("progress").val(transferedPercentage);
    videoElement.find(".progress").show();
    videoElement.find(".speed").html(downloadData['_speed_str']);

    console.log(msg)
});


$(document).ready(function () {
    $("#Downloading .deleteVideo").click(function () {
        var parentElement = $(this).parent();
        var videoId = parentElement.attr("video_id");

        $.post("/video/delete/"+videoId, function (data) {
            parentElement.remove();
        });
    });
});