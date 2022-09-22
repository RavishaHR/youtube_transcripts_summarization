function summFunc(){
    //Make the REST API call and get the summary

    //Show the summary to the user
    document.getElementById("summ").innerHTML = "aaaaaa";
    
}

function outputSummaryCallback(summary){

    console.log(summary);

    //Display the summary to the user
    document.getElementById('summ').innerHTML = summary;
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('summbutton')
    .addEventListener('click', function(){

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {message: "generate"}, function() {
                console.log("1");

            });
        });


        chrome.runtime.onMessage.addListener(
            function (request, sender, sendResponse) {
                
                console.log("2");
                outputSummaryCallback(request.action);
                //return true;
            }
        );

        

    });
});