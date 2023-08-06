import logging

def k8s_node_aws_instance_id(context: str, node: str):
  """
  На вход получается kubernetes Node ip-10-51-38-27.eu-west-1.compute.internal
  Необходимо получить AWS InstanceId
  Из API схемы получается строчка aws:///eu-west-1b/i-086fd4feb458ecde3
  Резлуьтат: i-086fd4feb458ecde3
  """
  provider_id = !(kubectl --context @(context) get node @(node) -o jsonpath="{.spec.providerID}")
  provider_id = str(provider_id)
  logging.debug(f"providerID {provider_id}")
  ec2_id = provider_id.split('/')[-1].replace('"', '')
  return ec2_id
