<html>
  <body>
    <form action="create_session" method="post" id="create_session">
      <b>Your name: </b> <input type"text" name="user_name" value="{{ username|default('', true) }}"/>
      <b>Create new session: </b> <input type"text" name="session_name"/>
      <input type="submit" name="action" value="create session"/>
    </form>
  </body>
</html>
