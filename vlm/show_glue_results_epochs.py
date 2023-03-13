import os
from pathlib import Path
from collections import defaultdict
import numpy as np
import re

root = Path(
    'snap'
)

task2major = {
    'QQP': 'acc_and_f1',
    'STS-B': 'corr',
    'MRPC': 'acc_and_f1',
}

# The tasks sorted by the amount of data
all_tasks = [
    # 'WNLI',
    'RTE',
    'MRPC',
    'STS-B',
    'CoLA',
    'SST-2',
    'QNLI',
    'QQP',
    'MNLI',
    'MNLI-MM',
]


def print_result(glue_dir):
    print(glue_dir)
    results = {}
    for task in glue_dir.iterdir():
        if task.is_dir():
            eval_fpath = task / 'eval_results.txt'
            task_name = task.name
            if eval_fpath.exists():
                with eval_fpath.open() as f:
                    for line in f:
                        metric, value = line.split('=')
                        metric = metric.strip()
                        value = float(value.strip())
                        if task_name in task2major:
                            if metric == task2major[task_name]:
                                results[task_name] = value
                        else:
                            results[task_name] = value
    if len(results) > 0:
        # sorted_keys = sorted(list(results.keys()))
        # for key in sorted_keys:
        #     print("%8s" % key, end='')
        # print("%8s" % 'GLUE', end='')
        # print()
        # for key in sorted_keys:
        #     print("%8.2f" % (results[key] * 100.), end='')
        # print("%8.2f" % (sum(results.values()) * 100. / len(results)), end='')
        # print()
        score = defaultdict(list)
        glue_score = defaultdict(list)
        glue4_score = defaultdict(list)
        number = ["9595", "9596", "9597", "9598", "9599"]
        for num in number:
            for result in results:
                if num in result:
                    glue_score[num].append(results[result]*100)
                    sub = re.sub("_\d{4}","",result)
                    if sub in ['QQP', 'QNLI', 'SST-2', 'MNLI']:
                        glue4_score[num].append(results[result]*100)
        for result in results:
            value = results[result]
            sub = re.sub("_\d{4}","",result)
            score[sub].append(value*100)
        print("|",end="")
        glue = ["WNLI", "MRPC", "STS-B", "CoLA", "MNLI-MM", "SST-2", "QNLI", "QQP", "MNLI"]
        for key in glue:
            print("", key, "|", end="")
        print("GLUE |",end="")
        print("<nobr>GLUE_4 |")
        print("|",end="")
        print(" -------- |"*(len(score)+2), end="")
        print()
        print("|",end="")
        for key in glue:
            mean = np.mean(np.array(score[key]))
            std = np.std(np.array(score[key]))
            print("<nobr>",round(mean,3),"±",round(std,3), "|", end="")
        glue_mean = []
        glue4_mean = []
        for key in glue_score:
            glue_mean.append(np.mean(np.array(glue_score[key])))
        for key in glue4_score:
            glue4_mean.append(np.mean(np.array(glue4_score[key])))
        print("<nobr>",round(np.mean(np.array(glue_mean)),3), "±", round(np.std(np.array(glue_mean)),3),"|",end="")
        print("<nobr>",round(np.mean(np.array(glue4_mean)),3), "±", round(np.std(np.array(glue4_mean)),3),"|")
        #print(score)


def search(path):
    def sorted_key(path):
        try:
            return path.stat().st_mtime
        except Exception:
            return 0.
    path_list = sorted(
        path.iterdir(),
        key=sorted_key
        # x.name
    )
    for subdir in path_list:
        #print(subdir)
        if subdir.is_dir():
            if 'glueepoch_' in subdir.name:
                print_result(subdir)
            else:
                search(subdir)

search(root)
