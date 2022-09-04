from django.db import models
from django.core import validators

from perffarm.validators import ValidateDate


class PgBenchBenchmark(models.Model):

    pgbench_benchmark_id = models.BigAutoField(primary_key=True)

    clients = models.IntegerField(validators=[validators.MaxValueValidator(50), validators.MinValueValidator(1)])
    scale = models.IntegerField(validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(1)])
    duration = models.IntegerField(validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(1)])
    read_only = models.BooleanField()

    class Meta:
        unique_together = ('clients', 'scale', 'duration', 'read_only')


class PgBenchResult(models.Model):

    pgbench_result_id = models.AutoField(primary_key=True)

    run_id = models.ForeignKey('runs.RunInfo', related_name='pgbench_result', on_delete=models.CASCADE)
    benchmark_config = models.ForeignKey('benchmarks.PgBenchBenchmark', on_delete=models.CASCADE, related_name='results')

    tps = models.FloatField(validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)])
    mode = models.CharField(max_length=100)
    latency = models.FloatField(validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(0)])
    start = models.FloatField()
    end = models.FloatField()
    iteration = models.IntegerField(validators=[validators.MinValueValidator(0)])
    init = models.FloatField(validators=[validators.MinValueValidator(0)])


class PgBenchRunStatement(models.Model):

    pgbench_run_statement_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', related_name='pgbench_run_statement', on_delete=models.CASCADE)
    line_id = models.IntegerField(null=True)
    latency = models.FloatField(null=True, validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(0)])
    result_id = models.ForeignKey('benchmarks.PgBenchStatement', on_delete=models.CASCADE)


class PgBenchStatement(models.Model):

    pgbench_statement_id = models.AutoField(primary_key=True)
    statement = models.TextField(null=True, unique=True)


class PgBenchLog(models.Model):

    pgbench_log_id = models.AutoField(primary_key=True)
    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='pgbench_log')

    interval_start = models.DateTimeField(null=True, validators=[ValidateDate])
    num_transactions = models.IntegerField(null=True, validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(0)])
    sum_latency = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(1000000), validators.MinValueValidator(0)])
    sum_latency_2 = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(1000000), validators.MinValueValidator(0)])
    min_latency = models.IntegerField(null=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    max_latency = models.IntegerField(null=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])


class PgStatStatementsQuery(models.Model):
    query_id = models.AutoField(primary_key=True)
    query = models.TextField()


class PgStatStatements(models.Model):
    pg_stat_statements_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='pg_stat_statements_iteration')
    query = models.ForeignKey('benchmarks.PgStatStatementsQuery', on_delete=models.CASCADE, related_name='pg_stat_statements_query')

    queryid = models.TextField(null=True)
    userid = models.IntegerField(null=True)
    dbid = models.IntegerField(null=True)
    plans = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    total_plan_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    min_plan_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    max_plan_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    mean_plan_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    stddev_plan_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    calls = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    total_exec_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    min_exec_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    max_exec_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    mean_exec_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    stddev_exec_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    rows = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    shared_blks_hit = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    shared_blks_read = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    shared_blks_dirtied = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    shared_blks_written = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    local_blks_hit = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    local_blks_read = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    local_blks_dirtied = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    local_blks_written = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    temp_blks_read = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    temp_blks_written = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    blk_read_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    blk_write_time = models.FloatField(validators=[validators.MinValueValidator(0)], null=True)
    wal_records = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    wal_fpi = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)
    wal_bytes = models.IntegerField(validators=[validators.MinValueValidator(0)], null=True)


class CollectdCpu(models.Model):
    collectd_cpu_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_cpu_iteration')

    percent_user = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_system = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_idle = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_wait = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_nice = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_interrupt = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_softirq = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
    percent_steal = models.FloatField(validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdProcess(models.Model):
    collectd_process_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_process_iteration')

    fork_rate = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_running = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_stopped = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_sleeping = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_paging = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_blocked = models.IntegerField(validators=[validators.MinValueValidator(0)])
    ps_state_zombies = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdContextswitch(models.Model):
    collectd_contextswitch_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_contextswitch_iteration')

    contextswitch = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdIpcShm(models.Model):
    collectd_ipc_shm_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_ipc_shm_iteration')

    segments = models.IntegerField(validators=[validators.MinValueValidator(0)])
    bytes_total = models.IntegerField(validators=[validators.MinValueValidator(0)])
    bytes_rss = models.IntegerField(validators=[validators.MinValueValidator(0)])
    bytes_swapped = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdIpcMsg(models.Model):
    collectd_ipc_msg_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_ipc_msg_iteration')

    count_space = models.IntegerField(validators=[validators.MinValueValidator(0)])
    count_queues = models.IntegerField(validators=[validators.MinValueValidator(0)])
    count_headers = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdIpcSem(models.Model):
    collectd_ipc_sem_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_ipc_sem_iteration')

    count_total = models.IntegerField(validators=[validators.MinValueValidator(0)])
    count_arrays = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdMemory(models.Model):
    collectd_memory_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_memory_iteration')

    memory_free = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    memory_used = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    memory_cached = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    memory_buffered = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    memory_slab_recl = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    memory_slab_unrecl = models.BigIntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdSwap(models.Model):
    collectd_swap_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_swap_iteration')

    swap_free = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    swap_used = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    swap_cached = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    swap_io_in = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    swap_io_out = models.BigIntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdVmem(models.Model):
    collectd_vmem_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_vmem_iteration')

    vmpage_number_active_file = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_inactive_file = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_isolated_file = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_active_anon = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_inactive_anon = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_isolated_anon = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_file_pages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_file_hugepages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_file_pmdmapped = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_kernel_stack = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_kernel_misc_reclaimable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_slab_reclaimable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_slab_unreclaimable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_write_pending = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_unevictable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_active_anon = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_inactive_anon = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_active_file = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zone_inactive_file = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_foll_pin_acquired = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_foll_pin_released = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_dirty = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_dirty_threshold = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_dirty_background_threshold = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_vmscan_write = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_vmscan_immediate_reclaim = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_anon_pages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_anon_transparent_hugepages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_shmem = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_shmem_hugepages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_shmem_pmdmapped = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_writeback = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_writeback_temp = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_free_pages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_free_cma = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_bounce = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_unevictable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_page_table_pages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_mapped = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_zspages = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_mlock = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_number_unstable = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_action_written = models.IntegerField(validators=[validators.MinValueValidator(0)])
    vmpage_action_dirtied = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class CollectdDisk(models.Model):
    collectd_disk_id = models.AutoField(primary_key=True)

    pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='collectd_disk_iteration')

    disk_octets_read = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    disk_octets_write = models.BigIntegerField(validators=[validators.MinValueValidator(0)])
    disk_merged_read = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_merged_write = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_ops_read = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_ops_write = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_io_time_io_time = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_io_time_weighted_io_time = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_time_read = models.IntegerField(validators=[validators.MinValueValidator(0)])
    disk_time_write = models.IntegerField(validators=[validators.MinValueValidator(0)])

    epoch = models.FloatField()


class BenchmarkType(models.Model):
    benchmark_type_id = models.AutoField(primary_key=True)
    benchmark_type = models.CharField(max_length=100)
