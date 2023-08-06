import json
import typing as t
import logging

from horbach_cli.libs.common_xsh import k8s_node_aws_instance_id

import typer
from rich import print

app = typer.Typer()


@app.command(help=":ship: сделать rollout restart workloads в ns")
def k8s_rollout_restart_ns(
    context: str = typer.Option(None, "--context", "-ctx", help="kubernetes context"),
    namespace: str = typer.Option("argocd", "--namespace", "-n", help="kubernetes namespace"),
):

    # Получаем список Подов в Неймспейсе
    k_all = !(kubectl --context @(context) -n @(namespace) get all --output json)
    k_all = str(k_all)
    k_all: dict = json.loads(k_all)["items"]
    workloads = [w["metadata"]["name"] for w in k_all if w["kind"] in ["Deployment", "StatefulSet"]]
    print(f"workloads to restart {workloads}")

    # Для каждого Пода в Неймспейсе делает РоллаутРестарт, если Овнер Деплой или Стс
    for obj in k_all:
      if obj["kind"] in ["Deployment", "StatefulSet"]:
        kubectl --context @(context) --namespace @(namespace) \
        rollout restart @(obj["kind"].lower()) @(obj["metadata"]["name"]) -o name


@app.command(help=":ship: сделать terminate Node")
def k8s_terminate_node(
    node: str = typer.Argument(None, help="kubernetes Node name"),
    context: str = typer.Option(None, "--context", "-ctx", help="kubernetes context"),
    profile: str = typer.Option("default", "--profile", "-p", help="aws named profile"),
    region: str = typer.Option("eu-west-1", "--region", "-r", help="aws region"),
):
  # ищем instance_id Node-ы
  ec2_id = k8s_node_aws_instance_id(context, node)
  print(f"node {node}, aws ec2 instance_id {ec2_id}")

  # дрейним, выключаем
  kubectl --context @(context) drain @(node) --delete-local-data --ignore-daemonsets --force
  aws ec2 terminate-instances --profile @(profile) --region eu-west-1 --instance-ids @(ec2_id) | jq


@app.command(help=":ship: подключиться к Node")
def k8s_ssm_node(
    node: str = typer.Argument(None, help="kubernetes Node name"),
    context: str = typer.Option(None, "--context", "-ctx", help="kubernetes context"),
    profile: str = typer.Option("default", "--profile", "-p", help="aws named profile"),
    region: str = typer.Option("eu-west-1", "--region", "-r", help="aws region"),
):
  # ищем instance_id Node-ы
  ec2_id = k8s_node_aws_instance_id(context, node)
  print(f"node {node}, aws ec2 instance_id {ec2_id}")

  # коннектимся по ssm
  aws ssm start-session --profile @(profile) --region @(region) --target @(ec2_id)


@app.command(help=":ship: список Pod-ов на Node-е")
def k8s_get_pods_on_node(
    node: str = typer.Argument(None, help="kubernetes Node name"),
    context: str = typer.Option(None, "--context", "-ctx", help="kubernetes context"),
):
  kubectl --context @(context) get pods -A --field-selector spec.nodeName=@(node)


@app.command(help=":ship: запечатать секрет в SealedSecret")
def k8s_kubeseal(
      context: str = typer.Option(None, "--context", "-ctx", help="kubernetes context"),
      file: str = typer.Option("config", "--file", "-f", help="kubernetes context"),
):
    kubeseal --context @(context) --controller-name sealed-secrets -o yaml \
    < @(file).secret.yml \
    > @(file).sealedsecret.yml


if __name__ == "__main__":
    app()
