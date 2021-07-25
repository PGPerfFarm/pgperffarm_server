const data = {
	links: [
        {
            name: 'HOME',
            url: '/index.html'
        },
        {
            name: 'MACHINES',
            url: '/machines/index.html'
        },
        {
            name: 'BENCHMARKS',
            url: '/benchmarks/index.html'
        }
    ]
};

const username = sessionStorage.getItem('user');

const template = (data) => `

<div id="navigation__title">PostgreSQL Performance Farm</div>

<div id="navigation__links">

    ${
        data.links
            .map((v) => `<a class="navigation__links__item" href="${v.url}">${v.name}</a>`)
            .join('')
    }

    ${
        username == null ?
        `<a id="navigation__links__login" href="${endpoints.login}">LOGIN</a>`:
        `<a id="navigation__links__login" href="/profile">${username}</a>`
    }

</div>

`;

// render
document.querySelector('#navigation').innerHTML = template(data);
