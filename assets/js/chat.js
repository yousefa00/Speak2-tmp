const table = document.querySelector('#msgTable');

function startTimer() {
  const seconds = 2000; //Refreshes every two seconds
  window.setTimeout(fetchMessage, seconds)
}

function fetchMessage() {
  fetch('/ajax/AjaxGetMessages')
    .then(function(response) {
      return response.json();
    })
    .then(function(myJson) {
      if (myJson.messages.length > 0){
        msgs = myJson
        table.innerHTML = "";
        for (let i = 0; i < msgs.messages.length; i++) {
          let row = table.insertRow()
          urlParams = new URLSearchParams(window.location.search);
          if (msgs.messages[i].sentTo == urlParams.get('id')){
            let cell = row.insertCell()
            cell.innerHTML = ""
            let cell2 = row.insertCell()
            cell2.innerHTML = msgs.messages[i].msg
            cell2.style.textAlign = "right"
          } else if (msgs.messages[i].sentTo == myJson.myId){
            let cell = row.insertCell()
            cell.innerHTML = msgs.messages[i].msg
            let cell2 = row.insertCell()
            cell2.innerHTML = ""
          }
        }
      }
      startTimer();
    })

}

fetchMessage()
