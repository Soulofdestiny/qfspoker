<html>
  <body>
    <h2> Hello {{name}}, Session {{session}} </h2>
    <textarea rows="4" cols="50" form="user_story" name="user_story" readonly="1">
    {{user_story}} 
    </textarea>
    <br>
    <input type="button" value="1 points" class="voteButton" data="1">
    <input type="button" value="2 points" class="voteButton" data="2">
    <input type="button" value="3 points" class="voteButton" data="3">
    <input type="button" value="5 points" class="voteButton" data="5">
    <input type="button" value="8 points" class="voteButton" data="8">
    <input type="button" value="13 points" class="voteButton" data="13">
    <br>
    <input type="button" value="< previous story" class="switch_story" data="prev_story">
    <input type="button" value="next story >" class="switch_story" data="next_story">
    <br>
    <br>
    <form action="import_story" method="post" id="import_story">
      <input type="submit" name="action" value="import_story"/>
      <input type"text" name="import_story"/>
    </form>

    <br>
    <h4>Currently there are {{ users|length }} users participating:</h4><br>
    <ul>
    {% for user in users %}
      <li> {{ user }} </li>
    {% endfor %}
    </ul>
  </body>
</html>
