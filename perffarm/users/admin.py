from django.contrib import admin

from machines.models import Machine
from runs.models import RunInfo, GitRepo, Branch, RunLog
from systems.models import HardwareInfo, Compiler, Kernel, OsDistributor, OsKernelVersion, OsVersion
from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchLog, PgBenchRunStatement,custom_query,InitSql,PgbenchCustomDetails,custom_queries
from tpch.models import TpchConfig, TpchResult, TpchQueryResult, TpchQuery, ExplainQueryCostOnResult, ExplainQueryCostOnResultDetails, ExplainQueryCostOffResult ,ExplainQueryCostOffPlan

# Register your models here.
admin.site.register(RunInfo)
admin.site.register(GitRepo)
admin.site.register(Branch)
admin.site.register(RunLog)

admin.site.register(HardwareInfo)
admin.site.register(Compiler)
admin.site.register(Kernel)
admin.site.register(OsDistributor)
admin.site.register(OsKernelVersion)
admin.site.register(OsVersion)

admin.site.register(PgBenchBenchmark)
admin.site.register(PgBenchResult)
admin.site.register(PgBenchStatement)
admin.site.register(PgBenchLog)
admin.site.register(PgBenchRunStatement)
admin.site.register(custom_query)
admin.site.register(InitSql)
admin.site.register(PgbenchCustomDetails)
admin.site.register(custom_queries)

admin.site.register(Machine)

admin.site.register(TpchConfig)
admin.site.register(TpchResult)
admin.site.register(TpchQueryResult)
admin.site.register(TpchQuery)
admin.site.register(ExplainQueryCostOnResult)
admin.site.register(ExplainQueryCostOnResultDetails)
admin.site.register(ExplainQueryCostOffResult)
admin.site.register(ExplainQueryCostOffPlan)



