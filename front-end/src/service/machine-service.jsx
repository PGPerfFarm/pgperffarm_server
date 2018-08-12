import PGUtil    from 'util/util.jsx'
import PGConstant from 'util/constant.jsx'
// const _const = new PGConstant();
const _util       = new PGUtil();

class MachineService{
    getMachineList(page){
        let url = PGConstant.base_url + '/machines';
        return _util.request({
            type    : 'get',
            url     : url,
            data    : {
                page : page
            }
        });
    }
}

export default MachineService;