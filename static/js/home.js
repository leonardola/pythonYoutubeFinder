$(function () {
    $(".download_path").change(function () {
        var that = $(this);

        $.post("/updateDownloadPath", {
            newDownloadPath: that.val()
        }, function () {
            that.addClass("done");
        })
    });
});