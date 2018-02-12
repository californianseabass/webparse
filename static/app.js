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
