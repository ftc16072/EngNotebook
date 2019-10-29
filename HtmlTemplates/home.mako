<%def name="title()">Home Page - ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<table>
<tr>
<th><button onclick= "window.location.href = '/newEntry';">Create New Entry</button></th>
<th><button onclick= "window.location.href = '/tasksForm';">Update/Add Tasks</button></th>
</tr>
<tr>
<th><button onclick= "window.location.href = '/viewEntries';">View Entries</button></th>
</tr>



</table>