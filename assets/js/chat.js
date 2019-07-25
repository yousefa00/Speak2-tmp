const table = document.querySelector('#msgTable');
var messages = []

function startTimer() {
  const seconds = 2000; //Refreshes every two seconds
  window.setTimeout(fetchMessage, seconds)
}

function fetchMessage() {
  urlParams = new URLSearchParams(window.location.search);
  fetch('/ajax/AjaxGetMessages?id=' + urlParams.get('id'))
    .then(function(response) {
      return response.json();
    })
    .then(function(myJson) {
      if (myJson.messages.length > 0){
        if (myJson.messages.length > messages.length){
          msgs = myJson

          for (let i = messages.length; i < msgs.messages.length; i++) {
            //<span class=""></span>
            let row = table.insertRow()
            if (msgs.messages[i].sentTo == urlParams.get('id')){
              let cell = row.insertCell()
              cell.innerHTML = ""
              let cell2 = row.insertCell()
              cell2.innerHTML = msgs.messages[i].msg
              cell2.style.textAlign = "right"
            } else if (msgs.messages[i].sentTo == myJson.myId){
              let icon = document.createElement("span");
              icon.className = "icon solid major fa-question"
              icon.style.display = 'inline-block'
              let cell = row.insertCell()
              //+ ", translated: " + msgs.messages[i].translated
              cell.innerHTML = msgs.messages[i].msg + " "
              cell.appendChild(icon)
              let italics = document.createElement("i")                // Create a <i> element
              let text = document.createTextNode(msgs.messages[i].translated);     // Create a text node
              italics.appendChild(text);                                   // Append the text to <i>
              cell.appendChild(italics);


              icon.onclick = function() {
                  if (italics.style.display === "none") {
                    italics.style.display = "block";
                  } else {
                    italics.style.display = "none";
                  }
               };

              let cell2 = row.insertCell()
              cell2.innerHTML = ""
            }
            messages.push(msgs.messages[i])
          }

        }
      }
      startTimer();
    })

}

fetchMessage()
