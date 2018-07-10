var http = new XMLHttpRequest();
var url = "/get_redmine_issue";


function get_redmine_issue()
{
    var story = document.querySelector('input#import_story').value;
    http.open("POST", url, true);
    console.log(story);
    
    http.send('import_story='.concat(story));
}

http.onreadystatechange = function() {
   if(http.readyState == 4 && http.status == 200) {
       user_story = document.querySelector('textarea#user_story');
       user_story.textContent = http.responseText;
   }
}
