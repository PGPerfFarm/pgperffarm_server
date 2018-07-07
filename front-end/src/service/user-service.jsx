import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'

const _util       = new PGUtil();

class User{
    login(loginInfo){
        let url = PGConstant.base_url + '/login/';
        return _util.request({
            type: 'post',
            url: url,
            data: loginInfo
        });
    }
    // check if the loginInfo is legel
    checkLoginInfo(loginInfo){
        let username = $.trim(loginInfo.username),
            password = $.trim(loginInfo.password);
        // check username
        if(typeof username !== 'string' || username.length ===0){
            return {
                status: false,
                msg: 'username cannot be an empty string!'
            }
        }
        // check password
        if(typeof password !== 'string' || password.length ===0){
            return {
                status: false,
                msg: 'password cannot be an empty string!！'
            }
        }
        return {
            status : true,
            msg : 'justify pass'
        }
    }
    // logout
    logout(){
        let url = PGConstant.base_url + '/logout';
        return _util.request({
            type    : 'post',
            url     : url
        });
    }

    getUserMachineManageList(pageNum){
        let url = PGConstant.base_url + '/my-machine';
        return _util.request({
            type    : 'get',
            url     : url,
            data    : {
                pageNum : pageNum
            }
        });
    }
}

export default User;