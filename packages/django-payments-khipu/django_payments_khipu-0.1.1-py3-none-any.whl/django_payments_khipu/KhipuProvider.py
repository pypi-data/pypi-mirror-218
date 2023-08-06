from django.http import JsonResponse
from payments import RedirectNeeded
from payments.core import BasicProvider


class KhipuProvider(BasicProvider):
    """docstring for KhipuProvider"""

    def __init__(self, key, **kwargs):
        super().__init__()
        self.key = key

    def get_form(self, payment, data=None):
        raise RedirectNeeded()

    def process_data(self, payment, request):
        return JsonResponse("process_data")

    def refund(self, payment, amount=None):
        return JsonResponse("refund")

    def capture(self, payment, amount=None):
        raise RedirectNeeded()

    def release(self, payment):
        raise NotImplementedError()
