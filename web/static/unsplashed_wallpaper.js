$(window).on('load', function () {
  var obj = {  
    method: 'GET'
  }

  fetch("/get_wallpaper?width=" + window.screen.width + "&height=" + window.screen.height , obj)
  .then(function(response) {
    return response.json();
  }).then(function(wallpaper_json) {
      $('#wallpaper_div').html('Photo taken by: ' + wallpaper_json['name']);
      $('#wallpaper_div').append('<img id="theImg" src="' + wallpaper_json['url'] + '" />');
  })
  .catch(function() {
    console.log("Something went wrong!");
  });
});
