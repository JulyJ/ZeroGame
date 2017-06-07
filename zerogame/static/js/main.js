$(document).ready(function(){
    try{
        var sock = new WebSocket('ws://' + window.location.host + '/ws');
    }
    catch(err){
        var sock = new WebSocket('wss://' + window.location.host + '/ws');
    }

    function showStory(story) {
        var storyElem = $('#subscribe'),
            height = 0,
            date = new Date();
            options = {hour12: false};
        storyElem.append($('<p>').html('[' + date.toLocaleTimeString('en-US', options) + '] ' + story + '\n'));
        storyElem.find('p').each(function(i, value){
            height += parseInt($(this).height());
        });

        storyElem.animate({scrollTop: height});
    }

    sock.onopen = function(){
        showStory('Let the story begins...')
    }

    sock.onmessage = function(event) {
      showStory(event.data);
    };

    $('#stop_journey').click(function(){
        window.location.href = "stop_journey"
    });

    sock.onclose = function(event){
        showStory('Story ended')
    };

    sock.onerror = function(error){
        showStory('Error:'+error);
    }
});
