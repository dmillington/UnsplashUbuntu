$(window).on('load', function () {
  var obj = {  
    method: 'GET'
  }

  fetch("/get_wallpaper?width=" + window.screen.width + "&height=" + window.screen.height , obj)
  .then(function(response) {
    return response.text();
  }).then(function(wallpaper_url) {
      $('#wallpaper_div').prepend('<img id="theImg" src="' + wallpaper_url + '" />');
  })
  .catch(function() {
    console.log("Something went wrong!");
  });
});
