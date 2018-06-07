import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'
const _util       = new PGUtil();

class Record{
    // get record list
    getRecordList(listParam){
        let url = PGConstant.base_url + '/records';

        let data = {};
        data.pageNum    = listParam.pageNum;

        return _util.request({
            type    : 'get',
            url     : url,
            data    : data
        });
    }

    // get record detail info
    getRecordInfo(recordId){
        let url = PGConstant.base_url + '/detail';

        return _util.request({
            type    : 'get',
            url     : '/detail',
            data    : {
                productId : recordId || 0
            }
        });
    }
}

export default Record;