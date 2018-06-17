from datetime import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
from users.models import UserProfile, UserMachine


class TestBranch(models.Model):
    """
    test brand
    """
    branch_name = models.CharField(max_length=128, verbose_name="branch name", help_text="branch name")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="branch added time",
                                    help_text="branch added time")

    class Meta:
        verbose_name = "test branch"
        verbose_name_plural = "test branch"

    def __str__(self):
        return self.branch_name


class TestCategory(models.Model):
    """
    tests category
    """
    cate_name = models.CharField(max_length=64, verbose_name="cate name", help_text="cate name")
    cate_sn = models.CharField(max_length=32, unique=True, verbose_name="cate sn", help_text="cate sn")
    # cate_parent = models.ForeignKey("self", verbose_name="parent category", related_name="sub_cat", help_text="parent category")
    cate_order = models.IntegerField(verbose_name="cate order", help_text="order in the current level")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="add time", help_text="category added time")

    class Meta:
        verbose_name = "tests category"
        verbose_name_plural = "tests category"

    def __str__(self):
        return self.cate_name


class PGInfo(models.Model):
    """
    pg info
    """
    pg_branch = models.ForeignKey(TestBranch, verbose_name="pg branch", help_text="pg branch")

    class Meta:
        verbose_name = "pg info"
        verbose_name_plural = "pg info"

    def __str__(self):
        return self.pg_branch


class MetaInfo(models.Model):
    """
    pg info
    """
    date = models.DateTimeField(verbose_name="date", help_text="date")
    uname = models.TextField(verbose_name="uname", help_text="uname")
    benchmark = models.TextField(verbose_name="benchmark", help_text="benchmark")
    name = models.TextField(verbose_name="name", help_text="name")

    class Meta:
        verbose_name = "meta info"
        verbose_name_plural = "meta info"


class LinuxInfo(models.Model):
    """
    linux info
    """
    mounts = models.TextField(verbose_name="mounts", help_text="mounts")
    cpuinfo = models.TextField(verbose_name="cpuinfo", help_text="cpuinfo")
    sysctl = models.TextField(verbose_name="sysctl", help_text="sysctl")
    meminfo = models.TextField(verbose_name="meminfo", help_text="meminfo")

    class Meta:
        verbose_name = "linux info"
        verbose_name_plural = "linux info"

    def __str__(self):
        return self.mounts


class TestRecord(models.Model):
    """
    tests
    """
    test_machine = models.ForeignKey(UserMachine, verbose_name="test owner",
                                     help_text="person who add this test item")
    pg_info = models.ForeignKey(PGInfo, verbose_name="pg info", help_text="pg info")
    meta_info = models.ForeignKey(MetaInfo, verbose_name="meta info", help_text="meta info")
    linux_info = models.ForeignKey(LinuxInfo, verbose_name="linux info", help_text="linux info")

    test_desc = models.TextField(verbose_name="test desc", help_text="test desc")
    # test_branch_id = models.ForeignKey(TestBranch, verbose_name="test category", help_text="test category")
    meta_time = models.DateTimeField(default=timezone.now, verbose_name="meta time")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="test added time")

    class Meta:
        verbose_name = "tests"
        verbose_name_plural = "tests"


# class AbstractTestDataSet(models.Model):
#     prev = models.ForeignKey('self',blank=True, null=True, related_name='none')
#     class Meta:
#         abstract = True

class TestDataSet(models.Model):
    test_record = models.ForeignKey(TestRecord, verbose_name="test record id", help_text="test record id")
    test_cate = models.ForeignKey(TestCategory, verbose_name="test cate id", help_text="test cate id")
    clients = models.IntegerField(verbose_name="clients", help_text="clients of the test dataset")
    scale = models.IntegerField(verbose_name="scale", help_text="scale of the test dataset")
    std = models.DecimalField(max_digits=18, decimal_places=8, verbose_name="std", help_text="std of the test dataset")
    metric = models.DecimalField(max_digits=18, decimal_places=8, verbose_name="metric",
                                 help_text="metric of the test dataset")
    median = models.DecimalField(max_digits=18, decimal_places=8, verbose_name="median",
                                 help_text="median of the test dataset")

    STATUS_CHOICE = (
        (-1, 'none'),
        (1, 'improved'),
        (2, 'quo'),
        (3, 'regressive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICE, verbose_name="status", help_text="status of this dataset")
    percentage = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="percentage",
                                     help_text="percentage compared to previous dataset")

    prev = models.ForeignKey('self', blank=True, null=True, related_name='prev1',
                             verbose_name="previous test dataset id", help_text="previous test dataset id")
    # prev = models.ForeignKey('self',verbose_name="previous test dataset id", help_text="previous test dataset id")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="test dataset time")

    class Meta:
        verbose_name = "test dataset"
        verbose_name_plural = "test dataset"


from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=TestDataSet)
def calc_status(sender, instance, **kwargs):
    print('dataset:' + str(instance.id) + "  prev:" + str(instance.prev) + " will be save ")

    # record_id = instance.test_record.id
    machine_id = instance.test_record.test_machine_id
    add_time = instance.test_record.add_time
    prevRecord = TestRecord.objects.order_by('-add_time').filter(test_machine_id=machine_id,
                                                                 add_time__lt=add_time).first()
    if (prevRecord == None):
        print("prev record not found")
        return
    print("previd is: " + str(prevRecord.id))
    prevTestDataSet = TestDataSet.objects.filter(test_record_id=prevRecord.id, scale=instance.scale,
                                                 clients=instance.clients, test_cate_id=instance.test_cate_id).first()

    if (prevTestDataSet == None):
        print("prev dataset not found")
        return

    print("prev dataset is: " + str(prevTestDataSet.id))

    percentage = (instance.metric - prevTestDataSet.metric)/prevTestDataSet.metric

    status = 0
    if(percentage >= 0.05):
        status = 1
    elif (percentage <= -0.05):
        status = 3
    else:
        status = 2

    instance.percentage = percentage
    instance.status = status
    instance.prev_id = prevTestDataSet.id
    # print instance
    # instance.save()
    return



class TestResult(models.Model):
    """
    test result sample:

    "latency": -1,
    "scale": "10",
    "end": 1526184453.133798,
    "clients": "2",
    "start": 1526184333.102856,
    "run": 0,
    "threads": "2",
    "mode": "simple",
    "duration": "120",
    "tps": "369.666116",
    "read-only": false

    """

    test_dataset = models.ForeignKey(TestDataSet, verbose_name="test dataset id", help_text="test dataset id")
    # test_cate = models.ForeignKey(TestCategory, verbose_name="test category", help_text="test category")
    latency = models.IntegerField(verbose_name="latency", help_text="latency of the test result")
    scale = models.IntegerField(verbose_name="scale", help_text="scale of the test result")
    end = models.DecimalField(max_digits=16, decimal_places=6, verbose_name="end",
                              help_text="endtime of the test result")
    clients = models.IntegerField(verbose_name="clients", help_text="clients of the test result")
    start = models.DecimalField(max_digits=16, decimal_places=6, verbose_name="start",
                                help_text="starttime of the test result")
    run = models.IntegerField(verbose_name="run", help_text="run number")
    threads = models.IntegerField(verbose_name="threads", help_text="threads of the test result")

    MODE_CHOICE = (
        (1, 'simple'),
    )
    mode = models.IntegerField(choices=MODE_CHOICE, verbose_name="mode", help_text="test mode")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="test result added time")

    class Meta:
        verbose_name = "test result"
        verbose_name_plural = "test result"
