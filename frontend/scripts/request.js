const getCookie = (name) => {
    const value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};

const sendRequest = (url, callback) => {

    const httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', url);
    httpRequest.withCredentials = true;
	httpRequest.send();

    httpRequest.onreadystatechange = () => {

        if (httpRequest.readyState === XMLHttpRequest.DONE) {

            if (httpRequest.status === 200 || httpRequest.status === 201) {
                const response = JSON.parse(httpRequest.response);
                callback(response);
            } 
            else {
                console.log(httpRequest.status);
            }

        }
        
    }

};

const sendPostRequest = (url, requestBody, callback) => {

    const csrftoken = getCookie('csrftoken');

    const httpRequest = new XMLHttpRequest();
    httpRequest.open('POST', url);
    httpRequest.withCredentials = true;
    httpRequest.setRequestHeader('X-CSRFTOKEN', csrftoken);
    httpRequest.send(JSON.stringify(requestBody));

    httpRequest.onreadystatechange = () => {
                    
        if (httpRequest.readyState === XMLHttpRequest.DONE) {

            if (httpRequest.status === 200 || httpRequest.status === 201) {
                callback();
            } else {
                console.log(httpRequest.status);
            }
            
        }

    }

};
