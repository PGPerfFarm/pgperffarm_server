import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'
const _util       = new PGUtil();

class Record{
    // get record list
    getRecordList(listParam){
        let url = PGConstant.base_url + '/records';

        let data = {};
        data = listParam;

        console.log('final data')
        console.dir(listParam);
        return _util.request({
            type    : 'get',
            url     : url,
            data    : data
        });
    }

    // get record detail info
    getRecordInfo(listParam){
        let url = PGConstant.base_url + '/detail/';
        url = url + listParam.recordNo
        return _util.request({
            type    : 'get',
            url     : url,
            // data    : {'Ldw7RrdP7jj4q89kgXCfeY'}
        });
    }
}

export default Record;