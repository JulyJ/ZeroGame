$(document).ready(function(){
    var sock = null;
    function connect() {
        disconnect();
        sock = new SockJS('http://' + window.location.host + '/ws', {debug: true});
        };

    function showStory(story) {
        var storyElem = $('#subscribe'),
            height = 0,
            date = new Date();
            options = {hour12: false};
        storyElem.prepend($('<p>').html('[' + date.toLocaleTimeString('en-US', options) + '] ' + story + '\n'));
        storyElem.find('p').each(function(i, value){
            height += parseInt($(this).height());
        });

        storyElem.animate({scrollBottom: height});
    }

    function disconnect() {
        if (sock != null) {
          log('Disconnecting...');
          sock.close();
          sock = null;
        }
      }

    connect();

    sock.onopen = function(){
        showStory('Let the story begins...')
    }

    sock.onmessage = function(event) {
        showStory(event.data);
    };

    $('#stop_journey').click(function(){
        window.location.href = "/stop_journey"
    });

    sock.onclose = function(){
        showStory('Story ended.')
        sock = null;
    };

    sock.onerror = function(error){
        showStory('Error');
        console.log(error);
        console.log(arguments)
    }
});
