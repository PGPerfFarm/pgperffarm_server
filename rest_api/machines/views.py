import hashlib
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from machines.models import Machine
from runs.models import RunInfo


@login_required
def add_machine_view(request):

    m = hashlib.md5()
    m.update(make_password(str(request.POST), 'pg_perf_farm').encode('utf-8'))
    machine_secret = m.hexdigest()

    machine = Machine(alias=request.POST['alias'], description=request.POST['description'], owner_id=request.user, machine_secret=machine_secret, approved=False)

    try:
        machine.save()
        return HttpResponse(text='Machine added successfully!', status=201)

    except Exception as e:
        return HttpResponse(status=400)


def machines_view(request):

    def get_latest(machine):

        run_info = RunInfo.objects.filter(machine_id=machine['machine_id']).order_by('-add_time').first()
        if run_info == None:
            return ''
        else:
            return run_info.run_id

    machines = Machine.objects.all().values('machine_id', 'alias', 'machine_type', 'add_time', 'description', 'approved', 'owner_id__username')
    machines_list = list(machines)

    for machine in machines_list:
        machine['latest'] = get_latest(machine)
    return JsonResponse(machines_list, safe=False)


@login_required
def my_machines_view(request):

    def get_latest(machine):

        run_info = RunInfo.objects.filter(machine_id=machine['machine_id']).order_by('-add_time').first()
        if run_info == None:
            return ''
        else:
            return run_info.run_id

    def get_count(obj):
        return RunInfo.objects.filter(machine_id=machine['machine_id']).count()

    my_machines = Machine.objects.filter(owner_id__username=request.user.username).values('machine_id', 'alias', 'machine_type', 'add_time', 'description', 'machine_secret', 'approved', 'owner_id__username', 'owner_id__email')
    my_machines_list = list(my_machines)

    for machine in my_machines_list:
        machine['latest'] = get_latest(machine)
        machine['count'] = get_count(machine)

    return JsonResponse(my_machines_list, safe=False)


def edit_machine_view(request, id):

    machine = Machine.objects.get(machine_id=id)

    if machine.owner_id_id == request.user.id:

        machine.description = request.POST.get('description')
        machine.save()
        return HttpResponse(status=201)

    else:
        return HttpResponse(status=403)
