const table = document.querySelector('#msgTable');

function startTimer() {
  const seconds = 2000; //Refreshes every two seconds
  window.setTimeout(fetchMessage, seconds)
}

function fetchMessage() {
  console.log("wow")
  fetch('/ajax/AjaxGetMessages')
    .then(function(response) {
      return response.json();
    })
    .then(function(myJson) {
      if (myJson.length > 0){
        console.log('bkafjknsdjfnjsdnfs')
        msgs = myJson
        table.innerHTML = "";
        for (let msgIndex in msgs) {
          let row = table.insertRow()
          urlParams = new URLSearchParams(window.location.search);
          if (msgs.messages[msgIndex].sendTo == urlParams.get('id')){
            let cell = row.insertCell()
            cell.innerHTML = ""
            let cell2 = row.insertCell()
            cell2.innerHTML = msgs.messages[msgIndex].msg
          } else {
            let cell = row.insertCell()
            cell.innerHTML = msgs.messages[msgIndex].msg
            let cell2 = row.insertCell()
            cell2.innerHTML = ""
          }
        }
      }
      startTimer();
    })

}

fetchMessage()
