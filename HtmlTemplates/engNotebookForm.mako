<%def name="title()">Entry Form-ftc16072</%def>
<%def name="head()">
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({ startOnLoad: false });
</script>
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
    <label for="taskId">What did you work on?</label> 
    <button onclick= "window.location.href = '/tasksForm';">Update/Add Tasks</button>
     <br/>
    <select name ="taskId">
        % for task in tasks:
            <option value=${task.taskId}>${task.name}</option>
        % endfor
    </select>
    <br/>
    <label for="hours">How many hours did you spend?</label><br/>
    <input type="number" name="hours" value="0" min="0" step="any" />
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
    <textarea name="notes" class="optional" rows="5" cols="30"></textarea>
    <br/>
    <label for="diagram">Diagram (using Mermaid):<a href="https://mermaid.live" target="_blank">Live Editor</a></label>
    <br/>
    <div>
    <textarea name="diagram" id="input" oninput="render()" class="optional" rows="8" cols="30" style="display:inline-block;vertical-align:top;"></textarea>
    <span id="graph" style="display:inline-block;vertical-align:top;">
    </span>
    </div>
    <P id="error-message" style="invisible;color: red"></P>
    <br/>
    <label for="photo">Photo?</label>
    <br/>
    <input name="photo" type="file" accept="image/*"/>
    <br/>
    <input type="submit" value="Submit">

</form>
<script type="text/javascript">
    rendering = false
    pendingUpdate = false
    diagramInput = document.getElementById('input')
    
function render() {
    src = diagramInput.value;
    if (!src) {
        return;
    }
    if (rendering) {
        pendingUpdate = true;
        return;
    }

    rendering = true;
    try{
        mermaid.render('theGraph', src, function(svgCode) {
            graph.innerHTML = svgCode;
        });
    }catch(err){
        graph.innerHTML = "<PRE>" + src + "</PRE>";
    }
    rendering = false;
    if (pendingUpdate) {
        pendingUpdate = false;
        render();
    }
}
</script>
