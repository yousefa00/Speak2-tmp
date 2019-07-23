function timedRefresh(timeoutPeriod) {
  setTimeout('location.reload(true)', timeoutPeriod);
}

window.onload = timedRefresh(10000);
