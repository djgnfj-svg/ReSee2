from reviewer.models import BackOfficeLogs
from accounts.models import MyUser
import json


class ShrinkersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.users_id = None
        if request.user.is_authenticated:
            get_user = MyUser.objects.filter(email=request.user).first()
            if get_user:
                request.users_id = get_user.id

        response = self.get_response(request)

        if request.method not in ["GET", "OPTIONS"]:
            try:
                body = request.POST if request.POST else None
            except json.decoder.JSONDecodeError:
                body = self.form_data_to_dict(request.POST)
            endpoint = request.get_full_path_info()
            ip = (
                request.headers["X-Forwarded-For"].split(",")[0]
                if "X-Forwarded-For" in request.headers.keys()
                else request.META.get("REMOTE_ADDR", None)
            )
            # X-Forwarded-For: <supplied-value>,<client-ip>,<load-balancer-ip>
            ip = ip.split(",")[0] if "," in ip else ip

            BackOfficeLogs.objects.create(
                endpoint=endpoint,
                body=body,
                ip=ip,
                user_id=request.users_id,
                status_code=response.status_code,
                method=request.method,
            )

        return response

    # @staticmethod
    # def form_data_to_dict(body: bytes):
    #     UNLOGGABLES = ["csrfmiddlewaretoken", "password"]
    #     body = body.decode("utf-8")
    #     body = unquote(body).split("&")
    #     rtn = {}
    #     for b in body:
    #         body_list = b.split("=")
    #         if body_list[0] not in UNLOGGABLES:
    #             rtn[body_list[0]] = body_list[1]
    #         else: 
    #             rtn[body_list[0]] = "hidden"
    #     return rtn