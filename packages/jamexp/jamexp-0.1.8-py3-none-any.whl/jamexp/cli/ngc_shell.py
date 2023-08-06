import itertools
import json
import os
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import click
import pandas as pd
import typer
from loguru import logger
from plumbum.commands.processes import ProcessExecutionError
from pyfzf.pyfzf import FzfPrompt

from jamexp.utils.os_shell import run_simple_command


@dataclass(order=True)
class BaseStatus:
    sort_index: int = field(init=False, repr=False)
    created_time: datetime
    queued_time: datetime
    started_time: datetime
    ended_time: datetime

    status: str
    job_id: str
    job_name: str
    device: str
    def __post_init__(self):
        self.sort_index = self.created_time
        if self.status == 'FINISHED_SUCCESS':
            if self.get_run_time() < timedelta(seconds=60 * 5):
                self.status = 'SHORT_RUN'

    def get_run_time(self):
        if self.status == 'RUNNING':
            return datetime.now(timezone.utc).replace(tzinfo=None) - self.started_time
        if self.status in ['FINISHED_SUCCESS', 'KILLED_BY_ADMIN']:
            if self.ended_time < datetime.max and self.started_time < datetime.max:
                return self.ended_time - self.started_time
        return timedelta(0)
    def get_queued_time(self):
        if self.status in ['QUEUED', 'RUNNING', 'FINISHED_SUCCESS']:
            return datetime.now(timezone.utc).replace(tzinfo=None) - self.queued_time
        return timedelta(999)

    def get_fzf_kv(self):
        run_time = self.get_run_time()
        base_kv = {
            'id': self.job_id,
            'status': self.status,
            'name': self.job_name,
            'run_time': f"{run_time.days}D{run_time.seconds//3600}H{(run_time.seconds//60)%60}M",
            'device': self.device,
        }
        return base_kv


    def get_ls_kv(self):
        base_kv = {
            'id': self.job_id,
            'name': self.job_name,
            'device': self.device,
        }
        run_time = self.get_run_time()
        if self.status in ['RUNNING','FINISHED_SUCCESS', 'KILLED_BY_ADMIN', 'KILLED_BY_USER']:
            base_kv['run_time'] = f"{run_time.days}D{run_time.seconds//3600}H{(run_time.seconds//60)%60}M"
        if self.status == 'QUEUED':
            queued_time = self.get_queued_time()
            base_kv['queued_time'] = f"{queued_time.days}D{queued_time.seconds//3600}H{(queued_time.seconds//60)%60}M"

        base_kv['created'] = self.created_time.strftime('%m-%d %H:%M')

        return base_kv

def parse_jobs(list_job):
    parsed_jobs = defaultdict(list)
    for job in list_job:
        status = job['jobStatus']['status']
        job_name = job['jobDefinition']['name']
        job_id = job['id']
        device = job['aceResourceInstance']
        created_time = datetime.strptime(job['jobStatus']['createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # parsing queued time
        if 'queuedAt' in job['jobStatus']:
            queued_time = datetime.strptime(job['jobStatus']['queuedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            queued_time = datetime.max
        # paraing started time
        if 'startedAt' in job['jobStatus']:
            started_time = datetime.strptime(job['jobStatus']['startedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            started_time = datetime.max
        # parsing ended time
        if 'endedAt' in job['jobStatus']:
            ended_time = datetime.strptime(job['jobStatus']['endedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            ended_time = datetime.max

        job = BaseStatus(created_time, queued_time, started_time, ended_time, status, job_id, job_name, device)

        parsed_jobs[job.status].append(job)

    return parsed_jobs

def ls_print_jobs(parsed_jobs, selected_status=None):
    sort_keys = {
        'RUNNING': 'run_time',
        'QUEUED': 'queued_time',
        'FINISHED_SUCCESS': 'id',
        'KILLED_BY_ADMIN': 'id',
        'KILLED_BY_USER': 'id',
    }
    # import ipdb; ipdb.set_trace()
    for status, jobs in parsed_jobs.items():
        if selected_status and status.lower() != selected_status.lower():
            continue
        print("#"*10 + f" {status}  Total {len(jobs):<10}" + "#"*10)
        if jobs:
            df = pd.DataFrame([job.get_ls_kv() for job in jobs]).sort_values(
                sort_keys.get(status, 'id'), ascending=False
            )
            print(df.to_string(index=False))

def collect_job(is_dir, key, ace='w2'):
    ace = {
        'w1': 'nv-us-west-1',
        'w2': 'nv-us-west-2',
        'w3': 'nv-us-west-3',
        'e1': 'nv-us-east-1',
        'e2': 'nv-us-east-2',
        'e3': 'nv-us-east-3',
    }[ace]
    team = 'deep-imagination' if is_dir else 'lpr-imagine'
    stdout, stderr = run_simple_command(f'ngc batch list --format_type json --team {team} --ace {ace}')
    if stderr:
        print('ngc batch list error')
        print(stderr)
    else:
        list_job = json.loads(stdout)
        parsed_jobs = parse_jobs(list_job)
        # filter jobs if key is not None and job_name has key
        if key:
            parsed_jobs = {k: [job for job in v if key in job.job_name] for k, v in parsed_jobs.items()}
    return parsed_jobs

def _ngc_list(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    ace : str = typer.Option("w2", help='ace number, default nv-us-west-2'),
    status : str = typer.Option('none', help='filter status, only show jobs whose status is the status'),
):
    status = None if status.lower() == 'none' else status
    parsed_jobs = collect_job(is_dir, key, ace)
    ls_print_jobs(parsed_jobs, status)

def _ngc_result(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    ace : str = typer.Option("w2", help='ace number, default nv-us-west-2'),
    is_fzf : bool = typer.Option(False, "-i/-I", help="use iteractive fzf to select job, default false -> use latest job"),
):
    parsed_jobs = collect_job(is_dir, key, ace)
    # parsed_jobs = {k: v if k in [] for k, v in parsed_jobs.items()}
    if 'QUEUED' in parsed_jobs:
        del parsed_jobs['QUEUED']
    if 'STARTING' in parsed_jobs:
        del parsed_jobs['STARTING']
    all_jobs = list(itertools.chain.from_iterable(parsed_jobs.values()))
    if len(all_jobs) == 0:
        logger.warning('no jobs found')
        return
    if is_fzf:
        df = pd.DataFrame([job.get_fzf_kv() for job in all_jobs]).sort_values('id', ascending=False)
        fzf_str = df.to_string(index=False).split('\n')
        try:
            fzf = FzfPrompt()
            select_run_str = fzf.prompt(fzf_str)[0]
            selected_id = int(select_run_str.split(' ')[0])
            select_run = [job for job in all_jobs if job.job_id == selected_id][0]
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
    else:
        latest_job = max(all_jobs, key=lambda x: x.job_id)
        if latest_job:
            select_run = latest_job
        else:
            exit(0)

    save_dir = os.path.expanduser("~/ngc_results")
    logger.warning(select_run)
    logger.warning(f'ngc result download {select_run.job_id} --dest {save_dir}')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    if os.path.exists(f"{save_dir}/{select_run.job_id}"):
        os.system(f'rm -rf {save_dir}/{select_run.job_id}')
    os.system(f'ngc result download {select_run.job_id} --dest {save_dir}')
    # print all files in the job dir
    dir_list = os.listdir(f"{save_dir}/{select_run.job_id}")
    for file_name in dir_list:
        logger.info(f"{save_dir}/{select_run.job_id}/{file_name}")

def _ngc_bash(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    ace : str = typer.Option("w2", help='ace number, default nv-us-west-2'),
    is_fzf : bool = typer.Option(False, "-i/-I", help="use iteractive fzf to select job, default false -> use latest job"),
):
    parsed_jobs = collect_job(is_dir, key, ace)
    all_jobs = []
    for k, v in parsed_jobs.items():
        if k in ['QUEUED', 'STARTING', 'RUNNING']:
            all_jobs.extend(v)
    if len(all_jobs) == 0:
        logger.warning('no job is running')
        return
    if is_fzf:
        df = pd.DataFrame([job.get_fzf_kv() for job in all_jobs]).sort_values('id', ascending=False)
        fzf_str = df.to_string(index=False).split('\n')
        try:
            fzf = FzfPrompt()
            select_run_str = fzf.prompt(fzf_str)[0]
            selected_id = int(select_run_str.split(' ')[0])
            select_run = [job for job in all_jobs if job.job_id == selected_id][0]
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
    else:
        latest_job = max(all_jobs, key=lambda x: x.job_id)
        if latest_job:
            select_run = latest_job
        else:
            exit(0)

    logger.warning(select_run)
    logger.warning(f"ngc batch exec {select_run.job_id}")
    while True:
        rtn_value = os.system(f"ngc batch exec {select_run.job_id}")
        if rtn_value != 0:
            logger.warning(f"ERROR VALUE {rtn_value}: ngc batch exec {select_run.job_id} failed, retrying...")
            time.sleep(5)
        else:
            break

def _ngc_kill(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    ace : str = typer.Option("w2", help='ace number, default nv-us-west-2'),
    is_fzf : bool = typer.Option(True, "-i/-I", help="use iteractive fzf to select job, default true. otherwise delete all jobs"),
    confirm : bool = typer.Option(False, "-c/-C", help="confirm to kill job, default false -> only print"),
):
    parsed_jobs = collect_job(is_dir, key, ace)
    all_jobs = []
    for k, v in parsed_jobs.items():
        if k in ['QUEUED', 'STARTING', 'RUNNING']:
            all_jobs.extend(v)
    if len(all_jobs) == 0:
        logger.warning('no job to be killed')
        return
    to_kill = []
    if is_fzf:
        df = pd.DataFrame([job.get_fzf_kv() for job in all_jobs]).sort_values('id', ascending=False)
        fzf_str = df.to_string(index=False).split('\n')
        try:
            fzf = FzfPrompt()
            select_runs_str = fzf.prompt(fzf_str, "-m")
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
        for select_run_str in select_runs_str:
            selected_id = int(select_run_str.split(' ')[0])
            to_kill.append([job for job in all_jobs if job.job_id == selected_id][0])
    else:
        to_kill = all_jobs
    df = pd.DataFrame([job.get_fzf_kv() for job in to_kill]).sort_values('id', ascending=False)
    logger.warning(f"will kill jobs. Confirmed : {confirm} ")
    print(df.to_string(index=False))
    if confirm:
        if click.confirm('Do you really want to kill?', default=True):
            for job in to_kill:
                logger.warning(f"ngc batch kill {job.job_id}")
                os.system(f"ngc batch kill {job.job_id}")

def ngc_list():
    typer.run(_ngc_list)

def ngc_result():
    typer.run(_ngc_result)

def ngc_kill():
    typer.run(_ngc_kill)

def ngc_bash():
    typer.run(_ngc_bash)
