from infratasks.utils.deployments import DeploymentsPaser, DeploymentHandler

dpl_key = "dpl"
deployments = DeploymentsPaser(dpl_key).get_parsed_elements()
DeploymentHandler().execute(None, deployments)

