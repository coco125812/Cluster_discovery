from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Node
import rest_framework
from django.utils import timezone

@api_view(['GET'])
def get_nodes(request):
    nodes = Node.objects.values('node_name', 'ip', 'is_master')
    return Response(nodes)

@api_view(['POST'])
def register_node(request):
    data = request.data

    node_name = data.get('nodeName')
    ip = data.get('ip')

    if not node_name or not ip:
        return Response({"error": "Invalid request"}, status=400)

    Node.objects.create(node_name=node_name, ip=ip, is_master=False)

    update_cluster_status()

    return Response({"message": "Node registered successfully", "clusterStatus": cluster_status})

@api_view(['POST'])
def deregister_node(request):
    data = request.data

    node_name = data.get('nodeName')
    ip = data.get('ip')

    if not node_name or not ip:
        return Response({"error": "Invalid request"}, status=400)

    try:
        node = Node.objects.get(node_name=node_name, ip=ip)
        is_master = node.is_master
        node.delete()
        update_cluster_status(is_master=is_master)

        return Response({"message": "Node deregistered successfully", "clusterStatus": cluster_status})

    except Node.DoesNotExist:
        return Response({"error": "Node not found"}, status=404)

@api_view(['POST'])
def heartbeat(request):
    data = request.data

    node_name = data.get('nodeName')
    ip = data.get('ip')

    if not node_name or not ip:
        return Response({"error": "Invalid request"}, status=400)

    try:
        node = Node.objects.get(node_name=node_name, ip=ip)
        node.last_heartbeat = timezone.now()
        node.save()

        update_cluster_status()

        return Response({"message": "Heartbeat received", "clusterStatus": cluster_status})

    except Node.DoesNotExist:
        return Response({"error": "Node not found"}, status=404)

@api_view(['POST'])
def vote(request):
    data = request.data

    node_name = data.get('nodeName')
    ip = data.get('ip')

    if not node_name or not ip:
        return Response({"error": "Invalid request"}, status=400)

    try:
        node = Node.objects.get(node_name=node_name, ip=ip)
      

        return Response({"message": "Vote cast successfully"})

    except Node.DoesNotExist:
        return Response({"error": "Node not found"}, status=404)

def update_cluster_status(is_master=False):
    global cluster_status

    nodes = Node.objects.all()

    if len(nodes) >= 3:
        if not is_master:
            master_node = max(nodes, key=lambda x: nodes.filter(is_master=True).count())
            master_node.is_master = True
            master_node.save()
        cluster_status = "GREEN"
    elif len(nodes) > 0:
        cluster_status = "YELLOW"
    else:
        cluster_status = "RED"
