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
                    <div class="col-lg-6">
                        <h4>Disabled Form States</h4>
                        <form role="form">
                            <fieldset disabled="">
                                <div class="form-group">
                                    <label for="disabledSelect">Disabled input</label>
                                    <input class="form-control" id="disabledInput" type="text" placeholder="Disabled input" disabled="">
                                </div>
                                <div class="form-group">
                                    <label for="disabledSelect">Disabled select menu</label>
                                    <select id="disabledSelect" class="form-control">
                                        <option>Disabled select</option>
                                    </select>
                                </div>
                                <div class="checkbox">
                                    <label>
                                        <input type="checkbox">Disabled Checkbox
                                    </label>
                                </div>
                                <button type="submit" class="btn btn-primary">Disabled Button</button>
                            </fieldset>
                        </form>
                        <h4>Form Validation States</h4>
                        <form role="form">
                            <div class="form-group has-success">
                                <label class="control-label" for="inputSuccess">Input with success</label>
                                <input type="text" class="form-control" id="inputSuccess">
                            </div>
                            <div class="form-group has-warning">
                                <label class="control-label" for="inputWarning">Input with warning</label>
                                <input type="text" class="form-control" id="inputWarning">
                            </div>
                            <div class="form-group has-error">
                                <label class="control-label" for="inputError">Input with error</label>
                                <input type="text" class="form-control" id="inputError">
                            </div>
                        </form>
                        <h4>Input Groups</h4>
                        <form role="form">
                            <div class="form-group input-group">
                                <span class="input-group-addon">@</span>
                                <input type="text" class="form-control" placeholder="Username">
                            </div>
                            <div class="form-group input-group">
                                <input type="text" class="form-control">
                                    <span class="input-group-addon">.00</span>
                            </div>
                            <div class="form-group input-group">
                                            <span class="input-group-addon"><i class="fa fa-eur"></i>
                                            </span>
                                <input type="text" class="form-control" placeholder="Font Awesome Icon">
                            </div>
                            <div class="form-group input-group">
                                <span class="input-group-addon">$</span>
                                <input type="text" class="form-control">
                                    <span class="input-group-addon">.00</span>
                            </div>
                            <div class="form-group input-group">
                                <input type="text" class="form-control">
                                            <span class="input-group-btn">
                                                <button class="btn btn-default" type="button"><i class="fa fa-search"></i>
                                                </button>
                                            </span>
                            </div>
                        </form>
                    </div>
                    {/*<!-- /.col-lg-12 -->*/}
                </div>
            </div>
        )
    }
}

export default Login;