alert("Running contentscript")
summary = "";

function reqListener (e) {
  summary = this.responseText;
  //sendmessage();
}

function reqFailed(e){
  alert(e);
}

function generateSummarycallback(){
  // - In call back function, extract the URL of the current tab and make a
  // GET HTTP request usingXMLHTTPRequestWeb API to the backend to receive
  // summarized text as a response.
  url = "http://localhost:5000/api/summarize?youtube_url=" + location.href


   

  const req = new XMLHttpRequest();
  req.addEventListener("load", reqListener);
  req.addEventListener("error", reqFailed);
  req.open("GET", url, true);
  req.send();
  
 


}

function sendmessage(){
  chrome.runtime.sendMessage({action: summary}, function() {
    //alert("Done");
  });
}



//- Add event listenerchrome.runtime.onMessageto listen
// messagegeneratewhich will execute thegenerateSummarycallback function.

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    //console.log(sender.tab ? "from a content script:" + sender.tab.url : "from the extension");

    if (request.message == "generate"){
      //REST API call
      generateSummarycallback();
      sendmessage();
      
    }
    //return true;
  }
    
    
);









