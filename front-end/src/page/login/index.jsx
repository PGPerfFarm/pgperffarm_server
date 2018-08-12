import React from 'react';
// import './index.css';
import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'
const _util = new PGUtil();
import User         from 'service/user-service.jsx'
const _user = new User();

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            redirect: _util.getUrlParam('redirect') || 'portal',
        }
    }

    componentWillMount() {
        document.title = 'LOGIN';
        let userinfo = _util.getStorage('userInfo')|| {};
        if(userinfo.token){
            this.props.history.push('/portal')
            // window.location.href = '/portal';
        }

    }

    onInputChange(e) {
        let inputValue = e.target.value,
            inputName = e.target.name;
        this.setState({
            [inputName]: inputValue
        });
    }

    onInputKeyUp(e) {
        if (e.keyCode === 13) {
            this.onSubmit();
        }
    }

    onSubmit() {
        let loginInfo = {
                username: this.state.username,
                password: this.state.password
            },
            checkResult = _user.checkLoginInfo(loginInfo);
        // check success
        if (checkResult.status) {
            _user.login(loginInfo).then((res) => {
                // console.dir(res)
                _util.setStorage('userInfo', res);
                // this.props.history.push(this.state.redirect);
                window.location.href = this.state.redirect;
            }, (err) => {
                // console.log(err)
                if (PGConstant.AuthorizedErrorCode === err) {
                    _util.errorTips('username or password is mistake!');
                }else{
                    _util.errorTips('login fail');
                }
            });
        }
        // check failure
        else {

            _util.errorTips(checkResult.msg);
        }

    }

    render() {
        return (
            <div id="page-wrapper">
                <div className="row">
                    <div className="col-lg-16">
                        <div className="panel panel-default">
                            <div className="panel-heading">
                                login to manage your machines!
                            </div>
                            <div className="panel-body">
                                <div className="row">
                                    {/*<!-- /.col-lg-6 (nested) -->*/}
                                    <div className="col-lg-12">
                                        <h4>Login Form</h4>
                                        <form role="form">
                                            <div className="form-group">
                                                {/*<label className="control-label" for="inputLogin"> login input</label>*/}
                                                <input type="text" className="form-control" id="inputLogin"
                                                       placeholder="Username or email"
                                                       name="username"
                                                       onKeyUp={e => this.onInputKeyUp(e)}
                                                       onChange={e => this.onInputChange(e)}/>
                                            </div>
                                            <div className="form-group">
                                                <input type="text" className="form-control" id="inputPwd"
                                                       name="password"
                                                       placeholder="password" onKeyUp={e => this.onInputKeyUp(e)}
                                                       onChange={e => this.onInputChange(e)}/>
                                            </div>
                                            <button type="button" className="btn btn-primary"  onClick={e => {this.onSubmit(e)}}>Button</button>
                                        </form>
                                    </div>
                                    {/*<!-- /.col-lg-6 (nested) -->*/}
                                </div>
                                {/*<!-- /.row (nested) -->*/}
                            </div>
                            {/*<!-- /.panel-body -->*/}
                        </div>
                        {/*<!-- /.panel -->*/}
                    </div>
                    {/*<!-- /.col-lg-12 -->*/}
                </div>
            </div>
        )
    }
}

export default Login;