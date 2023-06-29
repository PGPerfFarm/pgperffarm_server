from django.http import JsonResponse
from django.shortcuts import render
from machines.models import Machine
from runs.models import Branch, RunInfo
from tpch.models import TpchResult, TpchQueryResult
from tpch.models import ExplainQueryCostOffPlan, ExplainQueryCostOnResult, ExplainQueryCostOnResultDetails,ExplainQueryCostOffResult,TpchQuery
import json


def index(request):
    scale_groups = Machine.objects.raw("select machines_machine.machine_id, auth_user.username, Count(tpch_tpchresult.id), tpch_tpchconfig.scale_factor, machines_machine.alias, Max(runs_runinfo.add_time) last_run_time from tpch_tpchresult, tpch_tpchconfig, runs_runinfo, auth_user, machines_machine where tpch_tpchresult.run_id_id = runs_runinfo.run_id AND runs_runinfo.machine_id_id = machines_machine.machine_id AND machines_machine.owner_id_id = auth_user.id AND tpch_tpchresult.benchmark_config_id = tpch_tpchconfig.id GROUP  BY auth_user.username, tpch_tpchconfig.scale_factor, machines_machine.machine_id, machines_machine.alias")
    scale_groups = list(scale_groups)
    overview_json = {}
    for scale_g in scale_groups:
        if scale_g.scale_factor not in overview_json:
            overview_json[scale_g.scale_factor] = [scale_g]
        else:
            overview_json[scale_g.scale_factor].append(scale_g)

    queries=TpchQuery.objects.all().order_by('query_id')
    
    query_list = [{'query_id': q.query_id, 'query_statement': q.query_statement} for q in queries]
    return render(request, 'benchmarks/tpch.html', {'overview_json': overview_json, 'queries1':json.dumps(query_list),'queries':queries})


def trend(request, machine, scale):
    tpch_trends = Branch.objects.raw('SELECT machines_machine.alias, auth_user.username, runs_branch.branch_id, runs_runinfo.git_commit, tpch_tpchconfig.scale_factor, tpch_tpchconfig.streams, runs_branch.name, machines_machine.machine_id, Max(power_score)      max_power_score, Min(power_score)      min_power_score, Avg(power_score)      ave_power_score, Max(throughput_score) max_throughput_score, Min(throughput_score) min_throughput_score, Avg(throughput_score) ave_throughput_score, Max(composite_score)  max_composite_score, Min(composite_score)  min_composite_score, Avg(composite_score)  ave_composite_score FROM   auth_user, tpch_tpchresult, runs_branch, machines_machine, tpch_tpchconfig, runs_runinfo WHERE  auth_user.id = machines_machine.owner_id_id AND runs_runinfo.machine_id_id = machines_machine.machine_id AND runs_branch.branch_id = runs_runinfo.git_branch_id AND tpch_tpchresult.run_id_id = runs_runinfo.run_id AND tpch_tpchresult.benchmark_config_id = tpch_tpchconfig.id AND machines_machine.machine_id = %s AND tpch_tpchconfig.scale_factor = %s GROUP  BY auth_user.username, runs_runinfo.git_commit, tpch_tpchconfig.scale_factor, tpch_tpchconfig.streams, runs_branch.name, machines_machine.machine_id, runs_branch.branch_id, machines_machine.alias ', (machine, scale))
    tpch_trends_list = []

    for row in tpch_trends:
        pgbench_trend = {}
        for column in tpch_trends.columns:
            pgbench_trend[column] = getattr(row, column)
        tpch_trends_list.append(pgbench_trend)

    return render(request, 'benchmarks/tpch_trend.html', {'tpch_trends_list': tpch_trends_list})


def details(request, id):
    tpch_runs = Machine.objects.raw(
        'SELECT runs_runinfo.run_id, machines_machine.machine_id, machines_machine.alias, runs_runinfo.add_time, tpch_tpchconfig.scale_factor, tpch_tpchresult.power_score, tpch_tpchresult.throughput_score, tpch_tpchresult.composite_score, runs_runinfo.git_commit, runs_branch.name FROM   tpch_tpchresult, tpch_tpchconfig, machines_machine, runs_branch, runs_runinfo WHERE  runs_runinfo.machine_id_id = machines_machine.machine_id AND tpch_tpchresult.benchmark_config_id = tpch_tpchconfig.id AND runs_branch.branch_id = runs_runinfo.git_branch_id AND tpch_tpchresult.run_id_id = runs_runinfo.run_id AND runs_runinfo.run_id = %s', [id])
    tpch_runs_list = []
    for row in tpch_runs:
        single_run = {}
        for column in tpch_runs.columns:
            single_run[column] = getattr(row, column)
        tpch_runs_list.append(single_run)

    power_queries = TpchQueryResult.objects.raw("select tpch_tpchqueryresult.id, tpch_tpchqueryresult.query_idx, tpch_tpchqueryresult.time from tpch_tpchqueryresult, tpch_tpchresult where tpch_tpchqueryresult.tpch_result_id = tpch_tpchresult.id AND tpch_tpchresult.run_id_id = %s AND tpch_tpchqueryresult.type=%s", [id, 'power'])
    power_queries = list(power_queries)
    throughput_queries = TpchQueryResult.objects.raw("select tpch_tpchqueryresult.id, tpch_tpchqueryresult.query_idx, tpch_tpchqueryresult.time from tpch_tpchqueryresult, tpch_tpchresult where tpch_tpchqueryresult.tpch_result_id = tpch_tpchresult.id AND tpch_tpchresult.run_id_id = %s AND tpch_tpchqueryresult.type=%s", [id, 'throughput'])
    throughput_queries = list(throughput_queries)
    print(power_queries)
    models = []
    for i in range(0, len(power_queries)):
        models.append({
            "model_name": power_queries[i].query_idx,
            "field1": power_queries[i].time,
            "field2": throughput_queries[i].time
        })
    return render(request, 'benchmarks/tpch_details.html', { 'id':id, 'models': models, 'result': tpch_runs_list})


def runs_commit_view(request, machine, scale, commit):
    commit = '%' + commit

    tpch_runs = RunInfo.objects.raw("SELECT runs_runinfo.run_id, runs_runinfo.add_time FROM   tpch_tpchresult, machines_machine, runs_runinfo, tpch_tpchconfig WHERE  runs_runinfo.machine_id_id = machines_machine.machine_id AND runs_runinfo.run_id = tpch_tpchresult.run_id_id AND tpch_tpchresult.benchmark_config_id = tpch_tpchconfig.id AND runs_runinfo.machine_id_id = %s AND runs_runinfo.git_commit LIKE %s AND tpch_tpchconfig.scale_factor = %s ORDER  BY runs_runinfo.add_time DESC ", [machine, commit, scale])

    tpch_runs_list = []
    for row in tpch_runs:
        single_run = {}
        for column in tpch_runs.columns:
            single_run[column] = getattr(row, column)
        tpch_runs_list.append(single_run)

    return JsonResponse(tpch_runs_list, safe=False)



def explain_results(request,id):
    explain_results = {}

    Run_Info=RunInfo.objects.get(run_id=id)
    Tpch_Result=TpchResult.objects.get(run_id=Run_Info)

    Tpch_Query_Result_raw=TpchQueryResult.objects.filter(tpch_result=Tpch_Result)
    Tpch_Query_Result=[]
    for result in Tpch_Query_Result_raw:
       x=ExplainQueryCostOffResult.objects.filter(tpch_query=result)
       if(x is not None and len(x)>0):
              Tpch_Query_Result.append(result)
    
    # print(len(Tpch_Query_Result))
    Tpch_Query_Result.sort(key=lambda x: x.query_idx)
    

    # pass
   
    # Group the results by query_id
    for result in Tpch_Query_Result:
        query_id = result.query_idx
        if query_id not in explain_results:
            explain_results[query_id] = []
        x=ExplainQueryCostOffResult.objects.filter(tpch_query=result).all()
        for i in x:
          explain_results[query_id].append(i.plan_hash.result)

    Tpch_Querys=TpchQuery.objects.filter().all().order_by('query_id')
    context = {
        'explain_results': explain_results,
        'queries': Tpch_Querys,
    }

    return render(request, 'benchmarks/tpchCostOff.html', context)



def explain_results_CostOn(request,id):
    Run_Info=RunInfo.objects.get(run_id=id)
    Tpch_Result=TpchResult.objects.get(run_id=Run_Info)
    Tpch_Querys=TpchQuery.objects.filter().all().order_by('query_id')
    
    explain_results={}
    # models = []
    execution_time=[]
    planning_time=[]
    index=1;
    for query in Tpch_Querys:
        ExplainQuery_CostOnResult=ExplainQueryCostOnResult.objects.filter(tpch_query=query,tpch_result=Tpch_Result).first()
        if(ExplainQuery_CostOnResult is not None):
            execution_time.append(ExplainQuery_CostOnResult.execution_time)
            planning_time.append(ExplainQuery_CostOnResult.planning_time)
        index=index+1

    for query in Tpch_Querys:
        ExplainQuery_CostOnResult=ExplainQueryCostOnResult.objects.filter(tpch_query=query,tpch_result=Tpch_Result).first()
        if(ExplainQuery_CostOnResult is not None):
            data=ExplainQueryCostOnResultDetails.objects.filter(explain_query_cost_on_result=ExplainQuery_CostOnResult).all()
            explain_results[query.query_id] = []
            for x in data:
                result = x.result
                explain_results[query.query_id].append(result)
                
    
    # print(explain_results)
       



    return render(request, 'benchmarks/tpchCostOnTrands.html', { 'id':id, 'execution_time': execution_time,'planning_time':planning_time, 'explain_results': explain_results,'queries':Tpch_Querys})
    
    