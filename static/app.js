
t = 0;
let resp = "";
var converter = new showdown.Converter();

$(document).ready(function(){  
    $('#send').click(function(e){
        e.preventDefault();
        var prompt = $("#prompt").val().trimEnd();
        $("#prompt").val("");
        autosize.update($("#prompt"));

        $("#printout").append(
            "<div class='prompt-message'>" + 
            "<div style='white-space: pre-wrap;'>" +
            prompt  +
            "</div>" +
            "<span class='message-loader js-loading spinner-border'></span>" +
            "</div>"             
        );        
        // $(".border").animate({ scrollTop: $('.border').prop("scrollHeight")}, 1000);
        window.scrollTo({top: document.body.scrollHeight, behavior:'smooth' });

        runScript(prompt);  
        
        $(".js-logo").addClass("active");
    });     
    $('#prompt').keypress(function(event){        
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if((keycode == 10 || keycode == 13) && event.ctrlKey){
            $('#send').click();
            return false;
        }
    });       
    // $(function(){
    // var $overlay = $('#send'),
    //     $textarea = $('#prompt')
    // ;
    // $overlay.css({
    //         left: $textarea.width()-$overlay.width() + 'px',
    //         border: 0,
    //     });
    // });
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
            $("#printout").append(
                "<div class='px-3 py-3'>" + 
                "<div style='white-space: pre-wrap;'>" + 
                converter.makeHtml(data.response) + 
                "</div>" +
                " <small class='timer'>(" + t + "s)</small> " + 
                "</div>" 
            );           
        },
        error: function(data) {
            $("#printout").append(
                "<div class='text-danger response-message'>" + 
                "<div style='white-space: pre-wrap;'>" + 
                "There is a problem answering your question. Please check the command line output." + 
                "</div>" +
                " <small class='timer'>(" + t + "s)</small> " + 
                "</div>" 
            );              
        },
        complete: function(data) {
            clearInterval(myInterval);
            t = 0;
            $("#bot").addClass("fa-solid fa-ghost");
            $("#bot").removeClass("spinner-border");         
            $(".js-loading").removeClass("spinner-border");         
            // $(".border").animate({ scrollTop: $('.border').prop("scrollHeight")}, 1000);            
            window.scrollTo({top: document.body.scrollHeight, behavior:'smooth' });
            hljs.highlightAll(); 
            quote();                            
        }
    });   
}