const escapeHtml = (string) => {

    var entityMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;',
        '`': '&#x60;',
        '=': '&#x3D;'
    };

    return String(string).replace(/[&<>"'`=\/]/g, (s) => entityMap[s]);

};

const getUrlParam = (key) => {

    let params = location.search.substr(location.search.indexOf('') + 1);
    params = params.split('&');

    for(let i = 0; i < params.length; i++) {

        temp = params[i].split('=');

        if([temp[0]] == key) return temp[1];

    }

    return undefined;

};

const formatNumber = (number) => {

    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

};

const formatNumberRound = (number) => {

    return Number(number).toFixed(2);

};
