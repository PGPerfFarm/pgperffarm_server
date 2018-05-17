from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserProfile, UserMachine


class TestBranch(models.Model):
    """
    test brand
    """
    branch_name = models.CharField(max_length=128, verbose_name="branch name", help_text="branch name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="branch added time",
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
    # cate_parent = models.ForeignKey("self", verbose_name="parent category", related_name="sub_cat", help_text="parent category")
    cate_order = models.IntegerField(verbose_name="cate order", help_text="order in the current level")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time", help_text="category added time")

    class Meta:
        verbose_name = "tests category"
        verbose_name_plural = "tests category"

    def __str__(self):
        return self.cate_name


class Test(models.Model):
    """
    tests
    """
    test_name = models.CharField(max_length=128, verbose_name="test name", help_text="test name")
    test_desc = models.TextField(verbose_name="test desc", help_text="test desc")
    test_branch_id = models.ForeignKey(TestBranch, verbose_name="test category", help_text="test category")
    test_cate_id = models.ForeignKey(TestCategory, verbose_name="test category", help_text="test category")
    # test_item_id = models.CharField(max_length=32, unique=True, verbose_name="test sn", help_text="test sn")
    test_owner = models.ForeignKey(UserProfile, verbose_name="test owner", help_text="person who add this test item")
    test_machine_id = models.ForeignKey(UserMachine, verbose_name="test owner",
                                        help_text="person who add this test item")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="test added time")

    class Meta:
        verbose_name = "tests"
        verbose_name_plural = "tests"

    def __str__(self):
        return self.test_name
