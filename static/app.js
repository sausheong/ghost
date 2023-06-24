
t = 0;
let resp = "";

$(document).ready(function(){  
    $('#send').click(function(e){
        e.preventDefault();
        var prompt = $("#prompt").val().trimEnd();
        $("#prompt").val("");
        $("#printout").append(
            "<div class='px-3 py-2 text-primary-emphasis bg-light'>" + 
            "<pre style='white-space: pre-wrap;'>" +
            prompt  +
            "</pre>" +
            "</div>"             
        );        
        $(".border").animate({ scrollTop: $('.border').prop("scrollHeight")}, 1000);
        runScript(prompt);        
    });     
    $('#prompt').keypress(function(event){        
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if((keycode == 10 || keycode == 13) && event.ctrlKey){
            $('#send').click();
            return false;
        }
    });       
    $(function(){
    var $overlay = $('#send'),
        $textarea = $('#prompt')
    ;
    $overlay.css({
            left: $textarea.width()-$overlay.width() + 'px',
            border: 0,
        });
    });
    autosize($('#prompt'));    
});  

function runScript(prompt, action="/run") {
    function myTimer() {
        $("#bot").removeClass("fa-solid fa-ghost");
        $("#bot").addClass("spinner-border");   
        t++;
    }
    const myInterval = setInterval(myTimer, 1000);          
   
    $.ajax({
        url: action,
        method:"POST",
        data: JSON.stringify({input: prompt}),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(data){
            clearInterval(myInterval);
            $("#bot").addClass("fa-solid fa-ghost");
            $("#bot").removeClass("spinner-border");                          
            $("#printout").append(
                "<div class='px-3 py-2'>" + 
                "<pre style='white-space: pre-wrap;'>" + 
                data.response + 
                "</pre>" +
                " <small>(" + t + "s)</small> " + 
                "</div>" 
            );           
            $(".border").animate({ scrollTop: $('.border').prop("scrollHeight")}, 1000);
            t = 0;
            hljs.highlightAll();
        }
    });   
}