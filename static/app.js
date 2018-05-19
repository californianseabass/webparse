function save() {
	const url_to_save = document.getElementById('url_entry').value;
	fetch('/webparse/api/v0.1/pages', {
		body: JSON.stringify({url: url_to_save}),
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'user-agent': 'Mozilla/4.0 MDN Example',
		},
		credentials: 'same-origin', // include, *omit
		cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
		mode: 'cors', // no-cors, *same-origin
		redirect: 'follow', // *manual, error
		referrer: 'no-referrer', // *client
	}).then( response => {
		return response.json();
	}).then(res => {
		const url = res.url;
		const md5_hash = res.md5_hash;
		const backend_url = `/url/${md5_hash}`
		document.getElementById('frame').setAttribute('src', backend_url);
	})
}


function recursiveDeleteAllChildren(node){
	while (node.firstChild) {
		recursiveDeleteAllChildren(node.firstChild);
		document.removeChild(node.firstChild);
	}
	document.removeNode(node);
}

function search() {
    const searchPhrase = document.getElementById('search-box').value;
    const request = new URL('http://localhost:5000/webparse/api/v0.1/pages');
	request.searchParams.append('search-phrase', searchPhrase)
    fetch(request)
        .then(response => {
            return response.json();
        }).then(jsonData => {
			const searchResultsList = document.getElementById('search-results');
			oldListAnchor = document.querySelector('#search-results > ol')
			if (oldListAnchor) {
				oldListAnchor.remove();
			}
			previousListElements = document.querySelectorAll('#search-results > ol > li');
			if (previousListElements) {
				previousListElements.forEach(element => element.remove());
			}
			const listAnchor = searchResultsList.appendChild(
				document.createElement('ol')
			);
			let lastListElement = listAnchor;
			jsonData.forEach(data => {
				const newListElement = document.createElement('li');
				newListElement.appendChild(document.createTextNode(data.url));
				listAnchor.appendChild(newListElement);
			});
		});
}
