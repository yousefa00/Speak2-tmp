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

      startTimer();
    })

}

// let msgs = {{messages}}
// table1 = document.querySelector('#msgTable')
// for (let msgIndex in msgs) {
//   let row = table1.insertRow()
//   if (msgs[msgIndex].sendTo == urlParams.get('id')){
//     let cell = row.insertCell()
//     cell.innerHTML = ""
//     let cell2 = row.insertCell()
//     cell2.innerHTML = msgs[msgIndex].msg
//   } else {
//     let cell = row.insertCell()
//     cell.innerHTML = msgs[msgIndex].msg
//     let cell2 = row.insertCell()
//     cell2.innerHTML = ""
//   }
// }
