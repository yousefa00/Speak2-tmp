let link = document.querySelector('#search')
let input = document.querySelector('#searchInput')

link.addEventListener('click', ()=>{
	let searchVal = document.querySelector('#searchInput').value;
	window.location.href = "search?val=" + searchVal;
})

input.addEventListener('keypress', function (e) {
    var key = e.which || e.keyCode;
    if (key === 13) { // 13 is enter
			let searchVal = document.querySelector('#searchInput').value;
			window.location.href = "search?val=" + searchVal;
    }
});
