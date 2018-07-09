# -*- coding: UTF-8 -*-

"""
estimate dependent citations
"""

import os.path as op
import sys
from JamesLab.apps.base import ActionDispatcher, OptionParser
import pandas as pd

def main():
    actions = (
        ('DependentCitations', 'calculate dependent citations'),
        ('DownloadCitations', 'download all related citations from google scholar searching results'),
            )
    p = ActionDispatcher(actions)
    p.dispatch(globals())

def DependentCitations(args):
    """
    %prog AuthorsFile(copyied from GS profile) AllBibTexFile(including all citations in bibtex format)
    estimate how many dependent citations
    """
    p = OptionParser(DependentCitations.__doc__)
    opts, args = p.parse_args(args)

    if len(args) == 0:
        sys.exit(not p.print_help())
    AuthorsFile, AllBibTexFile, = args

    f1 = open(AllBibTexFile)
    titles, authors = [], []
    for i in f1:
        if '@' in i:
            tit = i.split('{')[-1].split(',')[0]
            titles.append(tit)
        elif '  author={' in i:
            aut = i.split('author={')[-1].split('}')[0]
            authors.append(aut)
    df = pd.DataFrame(dict(zip(['title', 'authors'], [titles, authors]))) 
    print('total %s citations in bibtex file'%df.shape[0])
    
    dependentPapers = []
    f2 = open(AuthorsFile)
    target_authors = f2.readline().split(', ')
    for i in target_authors:
        tar_a = set(i.split())
        for t,j in zip(df['title'], df['authors']):
            for k in j.split(' and '):
                obj_a = set(k.replace(',', ' ').split())
                if tar_a == obj_a:
                    dependentPapers.append(t)
    print('%s dependent citations'%len(set(dependentPapers)))

def DownloadCitations(args):
    pass

if __name__ == '__main__':
    main()