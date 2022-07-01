import hashlib
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from machines.models import Machine
from runs.models import RunInfo


def index(request):
    def get_latest(machine):
        run_info = RunInfo.objects.filter(machine_id=machine['machine_id']).order_by('-add_time')[:3].values('run_id')
        return [item['run_id'] for item in run_info]

    machines = Machine.objects.all().values('machine_id', 'alias', 'machine_type', 'add_time', 'description', 'approved', 'owner_id__username')
    machines_list = list(machines)

    for machine in machines_list:
        machine['latest'] = get_latest(machine)
        machine['next_url'] = '/benchmark/history/' + str(machine['machine_id']) + '/'

    return render(request, 'machines/index.html', {'machines': machines_list})

@login_required
def add_machine_view(request):
    body = request.POST
    m = hashlib.md5()
    m.update(make_password(str(body), 'pg_perf_farm').encode('utf-8'))
    machine_secret = m.hexdigest()
    machine = Machine(alias=body.get('alias'), description=body.get('description'), owner_id=request.user, machine_secret=machine_secret, approved=True)
    try:
        machine.save()
        return redirect('machines.index')

    except Exception as e:
        return HttpResponse(status=400)


@login_required
def approve_machine_view(request):

    body = json.loads(request.body)

    if request.user.is_staff:
        try:
            machine = Machine.objects.get(alias=body['alias'])
            machine.approved = True
            machine.save()

            return HttpResponse('Machine approved successfully!', status=201)

        except Machine.DoesNotExist:
            raise Http404()

    else:
        return HttpResponse(status=403)


def machines_view(request):

    def get_latest(machine):
        run_info = RunInfo.objects.filter(machine_id=machine['machine_id']).order_by('-add_time')[:3].values('run_id')
        return [item['run_id'] for item in run_info]

    machines = Machine.objects.all().values('machine_id', 'alias', 'machine_type', 'add_time', 'description', 'approved', 'owner_id__username')
    machines_list = list(machines)

    for machine in machines_list:
        machine['latest'] = get_latest(machine)
    return JsonResponse(machines_list, safe=False)


@login_required
def my_machines_view(request):

    def get_latest(machine):
        run_info = RunInfo.objects.filter(machine_id=machine['machine_id']).order_by('-add_time')[:3].values('run_id')
        return [item['run_id'] for item in run_info]

    def get_count(obj):
        return RunInfo.objects.filter(machine_id=machine['machine_id']).count()

    my_machines = Machine.objects.filter(owner_id__username=request.user.username).values('machine_id', 'alias', 'machine_type', 'add_time', 'description', 'machine_secret', 'approved', 'owner_id__username', 'owner_id__email')
    my_machines_list = list(my_machines)
    run_count = 0
    for machine in my_machines_list:
        machine['latest'] = get_latest(machine)
        cnt = get_count(machine)
        machine['count'] = cnt
        run_count += cnt
    print(my_machines_list)
    return render(request, 'machines/usermachine.html', {'my_machines_list': my_machines_list, 'run_count': run_count})


def edit_machine_view(request, id):

    body = json.loads(request.body)

    machine = Machine.objects.get(machine_id=id)

    if machine.owner_id_id == request.user.id:

        machine.description = body['description']
        machine.save()
        return HttpResponse(status=201)

    else:
        return HttpResponse(status=403)
