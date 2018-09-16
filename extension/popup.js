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
		fetch('http://127.0.0.1:8000/ranked', {
				method: 'PUT',
				headers: {
					"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
				},
				body: 'url=' + encodeURIComponent(url_path) + '&user=0',
			})
			.then(function(response) {
				// Examine the text in the response
				response.json().then(function(data) {
					ShowNewResults(data);
				});
			});
	});
}

function ShowNewResults(data) {
	document.body.style.width = '500px';
	real_button.style.display = 'none';
	fake_button.style.display = 'none';
	can_trust_button.style.display = 'none';
	var news = document.getElementById('results');
	markup_result = `
	<p>${data.result}</p>
	`
	if (data.doc.length > 0) {
		markup_1 = `
		<div class='center'>
		<p style='color: #333333' class='similar'><i>Based on the similar articles...</i></p>
		<div class='snippet ${data.doc[0].status}_snippet'>
		<a href="${data.doc[0].url}">
		<p>${data.doc[0].content}</p>
		<p class='credit'><i>${data.doc[0].friends[data.doc[0].friends.length-1]}</i></p>
		</a>
		</div>`
		markup_result += markup_1;
		if (data.doc.length == 2) {
			markup_2 = 
			`<div class='snippet ${data.doc[1].status}_snippet'>
			<a href="${data.doc[1].url}">
			<p>${data.doc[1].content}</p>
			<p class='credit'><i>${data.doc[1].friends[data.doc[1].friends.length-1]}</i></p>
			</a>
			</div>
			</div>`
			markup_result += markup_2;
		}
	}
	news.innerHTML = markup_result;
}
