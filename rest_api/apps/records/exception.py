# -*- coding: utf-8 -*-
class TestDataUploadError(RuntimeError):
  def __init__(self, arg):
   self.args = arg