import React from 'react';
// import './index.css';

class Login extends React.Component{
    render(){
        return (
            <div id="page-wrapper" >
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
                                                <input type="text" className="form-control" id="inputLogin" placeholder="Username or email"/>
                                            </div>
                                            <div className="form-group">
                                                <input type="text" className="form-control" id="inputPwd" placeholder="password"/>
                                            </div>
                                            <button type="submit" className="btn btn-primary">Button</button>
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