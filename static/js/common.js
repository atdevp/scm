function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getMaxNumber(s){
    d = parseInt(s)
    if (d < 10){
        s = "0" + s
    }else{
        s = s
    }
    return s
}

function formatTime(d){
    var time = d
    var data = new Date(time);  
    var year = data.getFullYear(); 
    var month = data.getMonth() + 1; 
    var day = data.getDate();
    var hours = data.getHours(); 
    var minutes = data.getMinutes();
    var seconds = data.getSeconds()
    t = getMaxNumber(year) + "-" + getMaxNumber(month) + "-" + getMaxNumber(day) + " " + getMaxNumber(hours) + ":" + getMaxNumber(minutes)+ ":" + getMaxNumber(seconds);
    return t
}