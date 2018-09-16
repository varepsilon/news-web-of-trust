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

can_trust_button.onclick = function(element) {
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tab => {
		var url_path = tab[0].url;
		console.log(url_path);
		fetch('http://127.0.0.1:8000/storage', {
				method: 'PUT',
				headers: {
					"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
				},
				body: 'url=' + encodeURIComponent(url_path),
			})
			.then(function(response) {
				// Examine the text in the response
				response.json().then(function(data) {
					ShowResults(data);
				});
			});
	});
}

function ShowResults(data) {
	document.body.style.width = '500px';
	var news = document.getElementById('results');
	for(var i = 0; i < data.length; i++) {
		var div = document.createElement("div");
		div.style.width = '150px';
		div.style.display = 'inline-block';
    		news.appendChild(div);
		var h5 = document.createElement("h5");
		h5.innerHTML = 'score: ' + data[i][0];
    		div.appendChild(h5);
		var p = document.createElement("p");
		p.innerHTML = data[i][1].doc.content
    		div.appendChild(p);
		for (const [user, ranking] of Object.entries(data[i][1].ranking)) {
			var p = document.createElement("p");
			p.innerHTML = user + ': ' + ranking
    			div.appendChild(p);
		}
	}
}
