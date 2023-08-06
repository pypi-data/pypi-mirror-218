from django.conf import settings
from threading import current_thread

Exclude_dir_patterns = ['/lib/python', '/middl_wares/', '/views.py', '/urls.py', '__init__.py',
                        '/serializers/']
Include_dir_patterns = [str(settings.BASE_DIR), ""]
Exclude_func_names = ['apply_async', 'before_start']
INCLUDE_EVENT_LIST = ['call', 'return', 'exception']

_requests_id = {}


def get_tracing_id():
    return _requests_id.get(current_thread().ident, None)


def set_tracing_id(value):
    _requests_id[current_thread().ident] = value


def get_class_name(frame):
    class_name = ''
    if 'self' or 'cls' in frame.f_locals:
        if 'self' in frame.f_locals:
            self_obj = frame.f_locals['self']
        elif 'self' in frame.f_locals:
            self_obj = frame.f_locals['cls']

        else:
            self_obj = None
        if hasattr(self_obj, '__class__'):
            class_name = self_obj.__class__.__name__
    return class_name


def extract_exception_info(arg):
    trace = []
    tb = arg[2]
    while tb is not None:
        trace.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "name": tb.tb_frame.f_code.co_name,
            "lineno": tb.tb_lineno
        })
        tb = tb.tb_next

    exception = {
        'type': type(arg[1]).__name__,
        'message': str(arg[0]),
        'trace': trace
    }
    return exception


def trace_func(frame, event, arg):
    if event in INCLUDE_EVENT_LIST:
        code = frame.f_code
        func_name = code.co_name
        file_name = frame.f_code.co_filename
        args = frame.f_locals

        if '__loader__' in args or '__module__' in args:
            return trace_func

        if list(filter(lambda x: x in file_name,
                       Exclude_dir_patterns)) or list(filter(lambda x: x not in file_name,
                                                             Include_dir_patterns)) or list(
            filter(lambda x: x in func_name,
                   Exclude_func_names)):
            return trace_func

        # filter event and find data
        class_name = get_class_name(frame)
        tracing_id = get_tracing_id()
        if event == 'call':
            data = {f"{func_name}": dict(file_name=file_name, class_name=class_name,
                                         values=args, tracing_id=tracing_id)}
        elif event == 'return':
            data = {f"{func_name}": dict(file_name=file_name, class_name=class_name,
                                         return_values=arg, tracing_id=tracing_id)}
        else:
            exception = extract_exception_info(arg)
            data = {f"{func_name}": dict(file_name=file_name, class_name=class_name,
                                         exception=exception, tracing_id=tracing_id)}

        print('data', data)
    return trace_func
