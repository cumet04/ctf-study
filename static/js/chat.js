window.addEventListener('load', () => {
    var form = document.querySelector('form');
    form.addEventListener("submit", (event) => {
        const form_data = new FormData(document.querySelector('form'));
        submit(form_data);
    });
    /*
    fetch(`./api/chat/posts`)
        .then((response) => {
            if (!response.ok) {
                console.log(`get API returns error: code=${response.status}, msg=${response.statusText}`)
                return;
            }
            response.json().then((result) => {
                show(result);
            });
        })
        .catch((error) => {
            console.log('There has been a problem with your fetch operation: ' + error.message);
        });
    */
});

function submit(form_data) {
    // get input data
    const name = form_data.get('name');
    const content = form_data.get('content');
    const submit_data = {
        'name': name,
        'content': content,
    };
    console.log(`submit data: ${submit_data}`)
    fetch(`./api/chat/posts`, {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify(submit_data)
    })
        .then((response) => {
            if (!response.ok) {
                console.log(`post API returns error: code=${response.status}, msg=${response.statusText}`)
                return;
            }
            response.json().then((result) => {
                show(result);
            });
        })
        .catch((error) => {
            console.log('There has been a problem with your fetch operation: ' + error.message);
        });
}

function show(result) {
    const tbody = document.getElementById('posts');
    while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
    result.posts.forEach((post, index) => {
        let td;
        let tr = document.createElement('tr');
        td = document.createElement('td');
        td.innerHTML = post.id;
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerHTML = post.timestamp;
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerHTML = post.name;
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerHTML = post.content;
        tr.appendChild(td);

        tbody.appendChild(tr);
    });
}