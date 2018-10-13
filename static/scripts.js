function openCity(evt, cityName)
{

    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");

    for (i = 0; i < tabcontent.length; i++)
    {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");

    for (i = 0; i < tablinks.length; i++)
    {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Execute when the DOM is fully loaded

$(document).ready(function()
{


    if(document.getElementById("rlogin") != null)
    {
        let form = document.getElementById("rlogin");
        form.onsubmit = function() {
            return (sanitycheck(form));
        };

        let form1 = document.getElementById("clogin");
        form1.onsubmit = function() {
            return (sanitycheck(form1));
        };

    }
    else
    {
        let form2 = document.getElementById("rregister");
        form2.onsubmit = function() {
            return (sanitycheck(form2));

        };

        let form3 = document.getElementById("cregister");
        form3.onsubmit = function() {
            return (sanitycheck(form3));

        };
    }



});

function sanitycheck(form)
{

            if (!form.username.value)
            {
                alert("missing username");
                return false;
            }
            else if (!form.password.value)
            {
                alert("missing password");
                return false;
            }
            else if (form.password.value != form.confirmation.value)
            {
                alert("passwords don't match");
                return false;
            }

            return true;

}

function callfunc(id)
{
    let parameters = {
        id : id
    };
    $.getJSON("/notice", parameters);
}

function callResolve(id)
{
    let parameters = {
        id : id
    };
    $.getJSON("/resolve", parameters);
}

function upload()
{
    $.getJSON("/uploadimg");
}
