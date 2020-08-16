<%def name="title()">FTC Notebook</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<form method="post" action="login">
    <input type="text" name="username" placeholder="Login Name"/>
    <br/><input type="password" name="password" placeholder="Password"/>
    <br/><input class="button" type="submit" value="Login" action="login" />
</form>