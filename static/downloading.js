
$(document).ready(function () {

    function getVideosStatus(){
        $.get("/videos", function (data) {
            showVideosData(data.data);
        });
    }

    getVideosStatus();

    setInterval(getVideosStatus,500);

    function showVideosData(videos){
        var html = '';

        var ejsData = new EJS({url: '/static/Templates/downloadingVideo.ejs.tmpl'});
        $('#renderPrice').html();

        for(var i in videos){
            if(!videos.hasOwnProperty(i)){
                continue;
            }else{
                var video = videos[i]
            }

            html += ejsData.render({video: video});
        }

        $("#Downloading").html(html);
    }
});