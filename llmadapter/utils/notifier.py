#TODO: backend imports

def send_setup_backend_notification(model_id, status, result):
    print("Notification Data:", result)
    #TODO: backend notification logic

def send_setup_notification(model_id, status):
    result = {}
    result['model_id'] = model_id
    result['status'] = status
    send_setup_backend_notification(model_id, status, result)
