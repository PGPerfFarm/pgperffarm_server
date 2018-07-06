
import PGConstant from 'util/constant.jsx'
// const _const = new PGConstant();
class PGUtil {
    request(param) {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: param.type || 'get',
                url: param.url || '',
                dataType: param.dataType || 'json',
                data: param.data || null,
                success: res => {
                    // request success

                    typeof resolve === 'function' && resolve(res, res.msg);
                    if (0 === res.status) {
                        typeof resolve === 'function' && resolve(res.data, res.msg);
                    }
                    // nologin force to login
                    else if (PGConstant.USER_UNLOGIN_CODE === res.status) {
                        this.doLogin();
                    }
                    else {
                        typeof reject === 'function' && reject(res.msg || res.data);
                    }
                },
                error: err => {
                    typeof reject === 'function' && reject(err.statusText);
                }
            });
        });
    }

    // redirect to login
    doLogin(){
        window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    }

    getUrlParam(name){
        // param=123&param1=456
        let queryString = window.location.search.split('?')[1] || '',
            reg         = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"),
            result      = queryString.match(reg);
        return result ? decodeURIComponent(result[2]) : null;
    }

    // success tips
    successTips(successMsg) {
        alert(successMsg);
    }

    // error tips
    errorTips(errMsg) {
        alert(errMsg);
    }

    // set local storage
    setStorage(name, data) {
        let dataType = typeof data;
        // json obj
        if (dataType === 'object') {
            window.localStorage.setItem(name, JSON.stringify(data));
        }
        // basical type
        else if (['number', 'string', 'boolean'].indexOf(dataType) >= 0) {
            window.localStorage.setItem(name, data);
        }
        // other unacceptable type
        else {
            alert('type unacceptabled');
        }
    }

    // get local storage
    getStorage(name) {
        let data = window.localStorage.getItem(name);
        if (data) {
            return JSON.parse(data);
        }
        else {
            return '';
        }
    }

    // remove local storage
    removeStorage(name) {
        window.localStorage.removeItem(name);
    }

    getDateStr(AddDayCount) {
        let dd = new Date();
        dd.setDate(dd.getDate()+AddDayCount);
        let y = dd.getFullYear();
        let m = (dd.getMonth()+1)<10?"0"+(dd.getMonth()+1):(dd.getMonth()+1);
        let d = dd.getDate()<10?"0"+dd.getDate():dd.getDate();
        return y+"-"+m+"-"+d;
    }
}

export default PGUtil;