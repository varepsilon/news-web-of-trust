let real_button = document.getElementById('real')
let fake_button = document.getElementById('fake')
let can_trust_button = document.getElementById('can_trust')

function SendVoteRequest(ranking) {
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tab => {
		var url_path = tab[0].url;
		fetch('http://127.0.0.1:8000/vote', {
			method: 'PUT',
			headers: {
				"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			body: 'url=' + encodeURIComponent(url_path) + '&user=Pasha&ranking=' + ranking,
		})
		.then(function(response) {
			console.log(response.status);
			console.log(response.statusText);
		});
	});
}

real_button.onclick = function(element) {
	SendVoteRequest('1');
}

fake_button.onclick = function(element) {
	SendVoteRequest('0');
}
