<%def name="title()">Entry Form-ftc16072</%def>
<%def name="head()">
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
<script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
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
    <textarea name="notes" class="optional" rows="5" cols="30"></textarea>
    <br/>
    <label for="diagramDot">Diagram (using Dot):<a href="https://graphs.grevian.org/example" target="_blank">Examples</a></label>
    <br/>
    <div>
    <textarea name="diagramDot" id="dotInput" oninput="render()" class="optional" rows="8" cols="30" style="display:inline-block;vertical-align:top;"></textarea>
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
    dotInput = document.getElementById('dotInput')
    var graphviz = d3.select("#graph").graphviz()
    .transition(function() {
        return d3.transition().duration(500);
    });
    
function render() {
    dotSrc = dotInput.value;
    if (!dotSrc) {
        return;
    }
    if (rendering) {
        pendingUpdate = true;
        return;
    }

    rendering = true;
    d3.select("#error-message").text("");
    graphviz
        .onerror(handleError)
        .renderDot(dotSrc, done);
}

function handleError(errorMessage) {
    // d3.select("#error-message").text(errorMessage);
    rendering = false;""
    if (pendingUpdate) {
        pendingUpdate = false;
        render();
    }
}    
function done() {
    rendering = false;
    if (pendingUpdate) {
        pendingUpdate = false;
        render();
    }
}
</script>
