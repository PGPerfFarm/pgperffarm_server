import PGUtil    from 'util/util.jsx'

const _util       = new PGUtil();

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