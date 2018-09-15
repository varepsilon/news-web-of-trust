let real_button = document.getElementById('real')
let fake_button = document.getElementById('fake')
let can_trust_button = document.getElementById('can_trust')

real_button.onclick = function(element) {
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tab => {
		var url = tab[0].url;
		alert(url);
		fetch('http://127.0.0.1:8000', {
			method='put',
			headers: {
				"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			body: 'url=http://google.com&user=u1&ranking=1.0'
		})
		.then(json)
		.then(function (data) {
			console.log('Request succeeded with JSON response', data);
		})
		.catch(function (error) {
			console.log('Request failed', error);
		});
	});
}
