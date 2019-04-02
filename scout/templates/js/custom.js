function searchBot(eve){
    console.log('clicked')
    var search_form = $(".keyword_search_form");
    $('[name="keywords"]').text($('[name="keywords"]').text().replace(/^\s+|\s+$/g, ''));
    var action = $(eve).attr("data-attrib-action");
    var name = $(eve).attr("data-attrib-name");
    console.log(eve)
    console.log(action)
    console.log(name)
    search_form.submit(function(onSubmit) {
        onSubmit.preventDefault();
    })
    if (action === "start"){     
        setTimeout(updateCounter, 7000);
        $(".alert.warning.search").hide()
        $(".alert.success.search").show()
        $("#start_search").attr("disabled", "disabled")
        $("#stop_search").attr("disabled", null)
    } else {
        $(".alert.warning.search").show()
        $(".alert.success.search").hide()
        $("#start_search").attr("disabled", null)
        $("#stop_search").attr("disabled", "disabled")
    }
    // Save Order
    jQuery.ajax({
        type: "POST",
        url: "/dashboard/",
        data: search_form.serialize() + "&action=" + action + "&name=" + name,
        success: function (response) {          
            if (action=="stop"){
                location.reload();
            }
        },
        error: function (errorObject, errorText, errorHTTP) {
            // console.log("Stopped")
        }
    });
}

function scoutBot(eve){
    var scout_form = $(".scout_form");
    $('[name="keylist"]').text($('[name="keylist"]').text().replace(/^\s+|\s+$/g, ''));
    var action = $(eve).attr("data-attrib-action");
    var name = $(eve).attr("data-attrib-name");
    console.log(eve)
    console.log(action)
    console.log(name)
    scout_form.submit(function(onSubmit) {
        onSubmit.preventDefault();
    })
    if (action === "start"){
        setTimeout(updateCounter, 7000);
        $(".alert.warning.scout").hide()
        $(".alert.success.scout").show()
        $("#start_scout").attr("disabled", "disabled")
        $("#stop_scout").attr("disabled", null)
    } else {
        $(".alert.warning.scout").show()
        $(".alert.success.scout").hide()
        $("#start_scout").attr("disabled", null)
        $("#stop_scout").attr("disabled", "disabled")
    }    
    // Save Order
    jQuery.ajax({
        type: "POST",
        url: "/dashboard/",
        data: scout_form.serialize() + "&action=" + action + "&name=" + name,
        success: function (response) {          
            if (action=="stop"){
                location.reload();
            }
        },
        error: function (errorObject, errorText, errorHTTP) {
            console.log("Stopped")
        }
    });
}

// Scout Data Table Initialization
$(document).ready(function() {
    $('#scout-results-table').DataTable({
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "language": {
            "search": "Filter results:",
            "lengthMenu": "Show Entries _MENU_"
          }
    });
    initializeVideo()
    updateCounter();
});


// Update Results Counter

function updateCounter(){
    jQuery.ajax({
        type: "GET",
        url: "/dashboard/stats/",
        success: function (data) {          
            console.log(data)
            // scout_table_body = $("#scout-results-table > tbody")
            $("#search-results-counter").html(data["search_status"])
            $("#scout-results-counter").html(data["scout_status"])
            console.log(data.search_stats)
            if (data.search_stats){
                $(".alert.warning.search").hide()
                $(".alert.success.search").show()
                $("#start_search").attr("disabled", "disabled")
                $("#stop_search").attr("disabled", null)
            } else {
                $(".alert.warning.search").show()
                $(".alert.success.search").hide()
                $("#start_search").attr("disabled", null)
                $("#stop_search").attr("disabled", "disabled")
            }
            if (data.scout_stats){
                $(".alert.success.scout").show()
                $(".alert.warning.scout").hide()
                $("#start_scout").attr("disabled", "disabled")
                $("#stop_scout").attr("disabled", null)
            } else {
                $(".alert.success.scout").hide()
                $(".alert.warning.scout").show()
                $("#start_scout").attr("disabled", null)
                $("#stop_scout").attr("disabled", "disabled")
            }
            if (data.search_status || data.scout_status){
                setTimeout(updateCounter, 7000)
            }
            return
        },
        error: function (errorObject, errorText, errorHTTP) {
            console.log("Stats could not be loaded")
        }
    });
}


var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};




// function submitDownloadRequest(event){
//     bot_name = $(event).attr("data-attrib-name")
//     console.log(bot_name)
//     if (bot_name === "scout"){
//         url = "scout/download/"
//     } else{
//         url = "asin/download/"
//     }
//     jQuery.ajax({
//         type: "POST",
//         url: url,
//         data: {csrfmiddlewaretoken: csrfcookie()},
//         success: function (data) {  
//             console.log("Download request submitted")
//             $( "html" ).replaceWith( data );
//         },
//         error: function (errorObject, errorText, errorHTTP) {
//             console.log("Download request could not be submitted")
//         }
//     });
// }


// function refreshDownloadRequest(){
//     url = location.href;
//     jQuery.ajax({
//         type: "GET",
//         url: url,
//         success: function (data) {  
//             if (data.length !== 0){
//                 window.open(url, '_blank');
//                 console.log("File downloaded successfully")
//             } else{
//                 setTimeout(downloadFile, 1500);
//                 // downloadFile(event, first=false)
//             }      
//             // console.log(data)
//         },
//         error: function (errorObject, errorText, errorHTTP) {
//             console.log("File could not be downloaded")
//         }
//     });
// }



// function downloadFile(event, first=true){
//     bot_name = $(event).attr("data-attrib-name")
//     console.log(bot_name, first)
//     if (bot_name === "scout"){
//         url = "scout/download/"
//     } else{
//         url = "asin/download/"
//     }
//     if (first === true){
//         type = "POST";
//     } else{
//         type = "GET";
//     }
//     console.log(type, url)
//     jQuery.ajax({
//         type: type,
//         url: url,
//         data: {csrfmiddlewaretoken: csrfcookie()},
//         success: function (data) {  
//             if (data.length !== 0){
//                 location.href=url
//             } else{
//                 setTimeout(downloadFile, 1500, event, false);
//                 // downloadFile(event, first=false)
//             }      
//             // console.log(data)
//         },
//         error: function (errorObject, errorText, errorHTTP) {
//             console.log("File could not be loaded")
//         }
//     });
// }

function initializeVideo() {
    // Gets the video src from the data-src on each button

    var $videoSrc;
    $(".video-btn").click(function () {
        $videoSrc = $(this).data("src");
    });
    console.log($videoSrc);

    // when the modal is opened autoplay it
    $("#videoModal").on("shown.bs.modal", function (e) {
        // set the video src to autoplay and not to show related video. Youtube related video is like a box of chocolates... you never know what you're gonna get
        $("#video").attr(
            "src",
            $videoSrc + "?rel=0&amp;showinfo=0&amp;modestbranding=1&amp;autoplay=1"
        );
    });

    // stop playing the youtube video when I close the modal
    $("#videoModal").on("hide.bs.modal", function (e) {
        // a poor man's stop video
        $("#video").attr("src", $videoSrc);
    });

    // document ready
}
