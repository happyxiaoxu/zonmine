// SignIn / Register Toggle

function hideLoginForm(elm=null){
    $('.login-form').hide()
    $('.register-form').show()
    $(".formHeading").text("Register")
  }

function hideSignupForm(elm=null){
      $('.register-form').hide()
      $('.login-form').show()
      $(".formHeading").text("Login")
  }

// Events
$('.login-form .message a').click(function(){
    $('.login-form').hide()
    $('.register-form').animate({height: "toggle", opacity: "toggle"}, "slow");
    $(".formHeading").text("Register")
 });
$('.register-form .message a').click(function(){
    $('.register-form').hide()
    $('.login-form').animate({height: "toggle", opacity: "toggle"}, "slow");
    $(".formHeading").text("Login")
 });

//Vertically centered modals
$(function() {
    function reposition() {
        var modal = $(this),
            dialog = modal.find('.modal-dialog');
        modal.css('display', 'block');
        
        // Dividing by two centers the modal exactly, but dividing by three 
        // or four works better for larger screens.
        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
    }
    // Reposition when a modal is shown
    $('.modal').on('show.bs.modal', reposition);
    // Reposition when the window is resized
    $(window).on('resize', function() {
        $('.modal:visible').each(reposition);
    });
});


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

initializeVideo()