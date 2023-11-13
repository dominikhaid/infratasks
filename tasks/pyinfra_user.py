from infratasks.utils.operations import OperationsPaser, OperationHandler

configure = True
delete = False
dpl_key = ""
ops_parser = OperationsPaser("ops")
ops_parser.add_element_from_name("user.pyinfra", configure, delete)
ops = ops_parser.get_parsed_elements()
OperationHandler.execute(None, ops)
