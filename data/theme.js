function setTheme(prefix)
{
    var theme = document.getElementById("theme");
    var buttons = document.getElementsByClassName("themebutton");

    if (localStorage.getItem("darkmode") === "true")
    {
        theme.href = prefix + "dark.css";
        for (var i = buttons.length; i > 0; i -= 1)
        {
            buttons[i-1].innerText = "Light Theme";
        }
    }
    else
    {
        theme.href = prefix + "default.css";
        for (var i = buttons.length; i > 0; i -= 1)
        {
            buttons[i-1].innerText = "Dark Theme";
        }
    }
}

function changeTheme(prefix)
{
    if (localStorage.getItem("darkmode") === "true")
    {
        localStorage.setItem("darkmode", "false");
    }
    else
    {
        localStorage.setItem("darkmode", "true");
    }
    setTheme(prefix);
}
