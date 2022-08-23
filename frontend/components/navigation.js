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
            .map((v) => `<a class="navigation__links__item" href="${v.url}"><button>${v.name}</button></a>`)
            .join('')
    }

    ${
        username == null ?
        `<a id="navigation__links__login" href="${endpoints.login}"><button>LOGIN</button></a>`:
        `<a id="navigation__links__login" href="/profile"><button>${username}</button></a>`
    }

</div>

`;

// render
document.querySelector('#navigation').innerHTML = template(data);
