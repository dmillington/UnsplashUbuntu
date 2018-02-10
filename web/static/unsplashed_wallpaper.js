$(window).on('load', function () {
  var obj = {  
    method: 'GET'
  }

  fetch("/get_wallpaper?width=" + window.screen.width + "&height=" + window.screen.height , obj)
  .then(function(response) {
    return response.json();
  }).then(function(wallpaper_json) {
      $('#wallpaper_div').html('Photo taken by: ' + wallpaper_json['name'] + ' on <a href="https://unsplash.com">Unsplash.com</a>');
      $('#wallpaper_div').append('<br/><img id="theImg" style="max-height: 1000px; max-width: 1000px;" src="' + wallpaper_json['url'] + '" />');
  })
  .catch(function() {
    console.log("Something went wrong!");
  });
});
