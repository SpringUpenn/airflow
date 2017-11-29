"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'istio_daily', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
generate_workflow_args = BashOperator(
    task_id='generate_workflow_args',
    bash_command='echo generate_workflow_args',
    dag=dag)

done = BashOperator(
    task_id='done',
    bash_command='echo done',
    dag=dag)
to_continue = BashOperator(
    task_id='to_continue',
    bash_command='echo to_continue',
    dag=dag)
run_release_qualification_tests = BashOperator(
    task_id='run_release_qualification_tests',
    bash_command='echo run_release_qualification_tests',
    dag=dag)
run_cloud_builder = BashOperator(
    task_id='run_cloud_builder',
    bash_command='echo run_cloud_builder',
    dag=dag)

github_release = BashOperator(
    task_id='github_release',
    bash_command='echo github_release',
    dag=dag)
github_tag_everything = BashOperator(
    task_id='github_tag_everything',
    bash_command='echo github_tag_everything',
    dag=dag)
push_release = BashOperator(
    task_id='push_release',
    bash_command='echo push_release',
    dag=dag)
start_release = BashOperator(
    task_id='start_release',
    bash_command='echo start_release',
    dag=dag)


run_cloud_builder.set_upstream(generate_workflow_args)
run_release_qualification_tests.set_upstream(run_cloud_builder)

to_continue.set_upstream(run_release_qualification_tests)
start_release.set_upstream(to_continue)
push_release.set_upstream(start_release)
github_release.set_upstream(push_release)
github_tag_everything.set_upstream(push_release)
done.set_upstream(github_release)
done.set_upstream(to_continue)