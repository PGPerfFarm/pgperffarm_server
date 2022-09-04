from django.contrib import admin

from machines.models import Machine
from runs.models import RunInfo, GitRepo, Branch, RunLog
from systems.models import HardwareInfo, Compiler, Kernel, OsDistributor, OsKernelVersion, OsVersion
from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchLog, PgBenchRunStatement

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

admin.site.register(Machine)
