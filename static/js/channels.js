$(document).ready(function () {

    $("#Add_new_channel_button").click(function (event) {
        event.stopPropagation();
        $("#New_channel").show();
    });

    $(document).click(function () {
        $("#New_channel").hide();
    });

    $("#New_channel").click(function (event) {
        event.stopPropagation();
    });

    $("#Channels .search_channel").click(function () {

        var channelName = $("#New_channel .new_channel_name").val();

        $.get("/channels/getDataByName/"+channelName, function (data) {
            var channels = data.data;

            var html = "";

            for(var i in channels){
                if(!channels.hasOwnProperty(i)){
                    continue;
                }else{
                    var channel = channels[i];
                }

                var image = channel['snippet']['thumbnails']['medium']['url'];
                var channelName = channel['snippet']['title'];
                var channelDescription = channel['snippet']['description'];
                var channelId = channel['id']['channelId'];

                html +=
                    '<option ' +
                            'image_src="'+image+'" ' +
                            'channel_id="'+channelId+'" ' +
                            'channel_description="'+channelDescription+'" ' +
                            'channel_id="'+channelId+'"'+
                            'channel_name="'+channelName+'">'+
                        channelName+
                    '</option>'
            }

            $("#New_channel .channels_list").html(html);
            $("#New_channel .channels_list").show();

            $("#Channels .channels_list").change();

        });
    });

    $("#Channels .channels_list").change(function () {
        var selectedOption = $(this).find(":selected");

        $("#New_channel img").attr("src",selectedOption.attr("image_src"));

        var description = getSelectedChannelDescripton(selectedOption);
        $("#New_channel .channel_description").html(description);

    });

    function getSelectedChannelDescripton(selectedOption){
        var description = selectedOption.attr("channel_description");

        return description || "No description provided";
    }


    $("#New_channel .add_channel").click(function () {
        var selectedChannel = $("#Channels .channels_list").find(":selected");

        var data =
        {
            id: selectedChannel.attr("channel_id"),
            image: selectedChannel.attr("image_src"),
            description: selectedChannel.attr("channel_description"),
            date: $("#New_channel .start_date").val(),
            name: selectedChannel.attr("channel_name"),
            unwanted_words:getUnwantedWords()
        };

        $.ajax({
            url: "/channel/add",
            type: "POST",
            contentType:"application/json",
            dataType: "json",
            data: JSON.stringify(data),
            success: function (data) {
                alert("success");
            }
        });
        //$.ajax("/channel/add",data, );
    });

    function getUnwantedWords(){
        var words = $("#New_channel .unwanted_words").val();

        return words.split(";");
    }
});