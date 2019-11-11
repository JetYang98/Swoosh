$(document).ready(function(){
    // 光标为pointer
    $(".input1").css("cursor", "pointer");
    $(".input1").attr("onmouseover", "input_over(this)");
    $(".input1").attr("onmouseout", "input_out(this)")
});

function input_over(self){
    self.style.textDecoration = "underline";
}

function input_out(self){
    self.style.textDecoration = null;
}