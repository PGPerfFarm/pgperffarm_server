import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'
// const _const = new PGConstant();
const _util       = new PGUtil();

class MachineService{
    getMachineList(pageNum){
        let url = PGConstant.base_url + '/machines';
        return _util.request({
            type    : 'get',
            url     : url,
            data    : {
                pageNum : pageNum
            }
        });
    }
}

export default MachineService;