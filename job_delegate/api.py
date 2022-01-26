from rest_framework import viewsets
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Job, SlaveServer
from django.conf import settings
import requests


@csrf_exempt
def domain_analysis(request):
    data = json.loads(request.body)

    # checking caches
    cache = Job.objects.filter(url=data['url'])
    if cache.exists():
        cache_result = json.loads(cache.last().result)
        if bool(cache_result):
            return JsonResponse(cache_result, status=200)

    # creating new Job instance
    client_instance = Job(ip=data['client']['ip'], url=data['url'], useragent=data['client']['useragent'])
    client_instance.save()

    # get status from all slave servers
    slaves_response = dict()
    headers = {"Authorization": "Bearer {}".format(client_instance.token)}
    for link in SlaveServer.objects.all():
        try:
            r = requests.get(link.url+'/status', headers=headers)
            print(r.text)
            slaves_response[link.url] = json.loads(r.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError):
            continue
    # ================================

    # defining most freedom slave server by queue and average processing time. Queue is priority
    slave_winner = dict()

    def change_slave_winner(new_obj: tuple):
        slave_winner['link'] = new_obj[0]
        slave_winner['queue'] = new_obj[1]['queue']['in_queue']
        slave_winner['average_processing_time'] = new_obj[1]['queue']['average_processing_time']

    for slave_obj in slaves_response.items():
        if not bool(slave_winner):
            change_slave_winner(slave_obj)
            continue
        if slave_winner['queue'] == slave_obj[1]['queue']['in_queue']:
            if float(slave_winner['average_processing_time']) > float(slave_obj[1]['queue']['average_processing_time']):
                change_slave_winner(slave_obj)
        if slave_winner['queue'] > slave_obj[1]['queue']['in_queue']:
            change_slave_winner(slave_obj)
    if not bool(slave_winner):
        return JsonResponse({'message': "Don`t have any slave servers", "type": "error"}, status=502)
    # ============================================================

    # send job to slave server
    request_data = {"job": {
        "url": data['url'],
        "id": client_instance.id,
        "priority": "normal",
        "callback": "{}/api/v1/callback/{}".format(settings.SITE_URL, client_instance.id)
    }}
    try:
        r = requests.post(slave_winner['link']+"/add-job", json=request_data, headers=headers)
        print(r.json())
    except requests.exceptions.ConnectionError:
        return JsonResponse({"message": "Something was wrong with slave server", "type": "error"}, status=502)
    # ======================
    return JsonResponse({"job": {"id": client_instance.id,
                                 "token": client_instance.token}, "queue": slave_winner['queue'] + 1}, status=200)


class Callback(viewsets.ModelViewSet):

    def post(self, request, pk):
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                job = Job.objects.get(pk=pk, token=token)
                job.result = json.dumps(request.data['results'])
                job.save()
                return JsonResponse({'message': 'OK', 'type': 'success'}, status=200)
            except Job.DoesNotExist:
                pass
        return JsonResponse({'message': 'Access denied', 'type': 'error'}, status=400)




@csrf_exempt
def report(request, pk, token):
    try:
        job = Job.objects.get(pk=pk, token=token)
        result = json.loads(job.result)
        if bool(result):
            return JsonResponse(json.loads(job.result), status=200)
        return JsonResponse({"message": "Job haven't done", "type": "warning"}, status=204)
    except Job.DoesNotExist:
        return JsonResponse({'message': "Job not founded!", 'type': "error"}, status=204)
