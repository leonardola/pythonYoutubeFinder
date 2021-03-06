$(document).ready(function () {

    $("#Add_new_channel_button").click(function (event) {
        event.stopPropagation();
        $("#New_channel").show();
    });

    $(document).click(function () {
        $("#New_channel").hide();
    });


    $("#New_channel .search_channel").click(function () {
        searchChannel();
    });

    $(document).keypress(function(e) {
        if(e.which == 13) {
            searchChannel();
        }
    });
    function searchChannel(){
        var channelName = $("#New_channel .new_channel_name").val();

        if(!channelName || !$("#New_channel").is(":visible")){
            return;
        }

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

            $("#New_channel .channels_list").change();

        });
    }

    $("#New_channel .thumbnail").click(function (event) {
        event.stopPropagation();
    });

    $("#New_channel .channels_list").change(function () {
        var selectedOption = $(this).find(":selected");

        $("#New_channel img").attr("src",selectedOption.attr("image_src"));

        var description = getSelectedChannelDescripton(selectedOption);
        var channelName = getSelectedChannelName(selectedOption);

        $("#New_channel h3").html(channelName);
        $("#New_channel .channel_description").html(description);

    });

    function getSelectedChannelDescripton(selectedOption){
        var description = selectedOption.attr("channel_description");

        return description || "No description provided";
    }

    function getSelectedChannelName(selectedOption){
        return selectedOption.attr("channel_name");
    }


    $("#New_channel .add_channel").click(function () {
        var selectedChannel = $("#New_channel .channels_list").find(":selected");

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
            contentType: "application/json",
            data: JSON.stringify(data),
        }).success(function () {
            location.reload();
        });
    });

    function getUnwantedWords(){
        var words = $("#New_channel .unwanted_words").val();

        if(!words){
            return [];
        }

        return words.split(";");
    }

    $("#Channels .remove_channel").click(function () {
        var channelBox = $(this).closest(".box");

        var channelId = channelBox.attr('channel_id');

        $.get("/channel/remove/"+channelId, function () {
            channelBox.remove();
        });
    });
});