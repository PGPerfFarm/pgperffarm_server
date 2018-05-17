class PGUtil{
    request(){
        //todo
    }
    // success tips
    successTips(successMsg){
        alert(successMsg);
    }
    // error tips
    errorTips(errMsg){
        alert(errMsg);
    }
    // set local storage
    setStorage(name, data){
        let dataType = typeof data;
        // json obj
        if(dataType === 'object'){
            window.localStorage.setItem(name, JSON.stringify(data));
        }
        // basical type
        else if(['number','string','boolean'].indexOf(dataType) >= 0){
            window.localStorage.setItem(name, data);
        }
        // other unacceptable type
        else{
            alert('type unacceptabled');
        }
    }
    // get local storage
    getStorage(name){
        let data = window.localStorage.getItem(name);
        if(data){
            return JSON.parse(data);
        }
        else{
            return '';
        }
    }
    // remove local storage
    removeStorage(name){
        window.localStorage.removeItem(name);
    }
}

export default PGUtil;