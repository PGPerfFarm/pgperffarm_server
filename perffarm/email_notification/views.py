from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from benchmarks.models import BenchmarkType
from email_notification.models import EmailNotification


@login_required
def update_email_notification_view(request):
    body = request.POST
    email_pgbench = EmailNotification.objects.get(owner=request.user, type=BenchmarkType.objects.get(benchmark_type_id=1))
    email_pgbench.is_active = True if body.get("noti_pgbench") == "on" else False
    email_pgbench.threshold = body.get("threshold_pgbench")
    email_tpch = EmailNotification.objects.get(owner=request.user, type=BenchmarkType.objects.get(benchmark_type_id=2))
    email_tpch.is_active = True if body.get("noti_tpch") == "on" else False
    email_tpch.threshold = body.get("threshold_tpch")
    try:
        email_pgbench.save()
        email_tpch.save()
        return redirect('/machine/user')
    except Exception as e:
        return HttpResponse(status=400)
