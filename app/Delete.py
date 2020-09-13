#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.Dates import Labels
from app.Occurence_class import Occurences, Occurence_List


class Delete:
    Labels.delete()
    Occurences.delete()
