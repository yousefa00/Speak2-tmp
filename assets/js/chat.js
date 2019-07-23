const table = document.querySelector('#msgTable');

function startTimer() {
  const seconds = 2000; //Refreshes every two seconds
  window.setTimeout(fetchMessage, seconds)
}

function fetchMessage() {
  console.log("wow")
  fetch('/ajax/AjaxGetMessages')
    .then(function(response) {
      console.log("5")
      return response.json();
    })
    .then(function(myJson) {
      console.log(myJson.messages)
      console.log(myJson.messages.length)
      if (myJson.messages.length > 0){
        console.log('bkafjknsdjfnjsdnfs')
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
          } else {
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
