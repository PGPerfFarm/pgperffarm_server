import Util    from 'util/util.jsx'

const _util       = new Util();

class Status{
    // get status list
    getStatusList(listParam){
        let url     = '',
            data    = {};

        //todo
        return _util.request({
            type    : 'post',
            url     : url,
            data    : data
        });
    }
}

export default Status;