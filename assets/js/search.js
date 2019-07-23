let link = document.querySelector('#search')

link.addEventListener('click', ()=>{
	let searchVal = document.querySelector('#searchInput').value;
	console.log("testtstdtvff")
	window.location.href = "search?val=" + searchVal;
})
