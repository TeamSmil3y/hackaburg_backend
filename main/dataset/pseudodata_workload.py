import math
import random

from ..models import Hub, Company
from random import uniform, randint

def f(x, k=100):
    a = lambda x: math.exp(-(x**4))
    return k * a((x-12)/5) - .2*k* a((x-12)/2)

def create_pseudodata():
    for company in Company.objects.all():
        workload = []
        for day in range(7):
            workload_day = []
            x_offset = uniform(-0.5, 0.5)
            x_scale = uniform(0.9, 1.1)
            y_scale = uniform(0.9, 1.1)
            
            if day == 6 or (day == 5 and random.randint(0,5) == 3):
                y_scale = 0
                
            
            for i in range(24):
                v = int(y_scale*(f((i+0.5+x_offset)*x_scale) + randint(-3, 3)))
                if v < 0:
                    v = 0
                workload_day.append(v)
            
            
            workload.append(workload_day)
        
        company.workload = ";".join([",".join(map(str, j)) for j in workload])
        company.save()
        
        