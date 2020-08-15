<%def name="title()">Entry Form-ftc16072</%def>
<%def name="head()">
<link rel="stylesheet" type="text/css"
  href="/static/mathquill.css" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="/static/mathquill.js"></script>
</%def>
<%inherit file = "base.mako"/>
<a href="index">Back<a>
<form action="addEntry" method="post" enctype="multipart/form-data">
    <label for="date">Date (yyyy-mm-dd):</label>
    <input type="date" name="dateString" value='${dateString}' required pattern="\d{4}-\d{2}-\d{2}"/>
    <br/>
    <label for="memberId">Your Name:</label> 
    <select name ="memberId" required>
        <option value=""> Select a name </option>
        % for member in members:
            <option value=${member.memberId}>${member.name}</option>
        % endfor
    </select>
    <br/>
    <label for="taskId">What did you work on?</label> <br/>
    <select name ="taskId">
        % for task in tasks:
            <option value=${task.taskId}>${task.name}</option>
        % endfor
    </select>
    <br/>
    <label for="accomplished">What did you do?</label>
    <br/>
    <textarea name="accomplished" rows="5" cols="30"></textarea>
    <br/>
    <label for="why"> Why did you do that? </label>
    <br/>
    <textarea name="why" rows="5" cols="30"></textarea>
    <br/>
    <label for="learning">What did you learn?</label>
    <br/>
    <textarea name="learning" rows="5" cols="30"></textarea>
    <br/>
    <label for="next_steps">Next Steps?</label>
    <br/>
    <textarea name="next_steps" rows="5" cols="30"></textarea>
    <br/>
    <label for-"notes"> Notes: </label>
    <br/>
    <textarea name="notes" rows="5" cols="30"></textarea>
    <br/>
    <p>Type math here: <span id="equations" class="mathquill-math-field"></span></p>
    <input type="hidden" id="latexInput" name="latexInput" value=""/> 
    <br/>
    <label for="photo">Photo?</label>
    <br/>
    <input name="photo" type="file" accept="image/*"/>
    <br/><br/>
    <input type="submit" value="Submit">

</form>
<script type="text/javascript">
  var MQ = MathQuill.getInterface(MathQuill.getInterface.MAX);
  var equationSpan = document.getElementById('equations');
  var latexInput = document.getElementById('latexInput');

  var equationMathField = MQ.MathField(equationSpan, {
    handlers: {
      edit: function() {
        latexInput.value = equationMathField.latex(); 
      }
    }
  });
  equationMathField.latex(latexInput.value)
</script>