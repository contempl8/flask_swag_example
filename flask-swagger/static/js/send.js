function buttonAction()
{
    const name = document.getElementById("button0").innerHTML
    console.log(name)
    $.ajax({
        url: '/HomeSpace/button_actions',
        type: 'PUT',
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            var0: 1000,
            unexpected: "Thing"
        }),
        success: function (response) {
            console.log("Success Callback")
        },
        error: function (response) {
            console.log("Error Callback")
        }
    });

};

function send_request(method,url,data)
{
    let xhttp = new XMLHttpRequest();
    xhttp.open(method,url,false);
    if ( method == "PUT" ) {
        xhttp.setRequestHeader('Content-Type','application/json');
    }
    xhttp.send(data);
    ret = "";
    if(xhttp.readyState == 4 && xhttp.status == 200)
      ret = xhttp.responseText;
    else
      alert("CGI '" + uri + "' failed!");

    return ret;
}

async function buttonGet() {
    await send_request("GET",'/HomeSpace/button_actions');
}

async function buttonPut() {
    await send_request("PUT",'/HomeSpace/button_actions',"{\"var0\":1000}");
}
