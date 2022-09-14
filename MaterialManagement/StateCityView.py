from django.http import JsonResponse
from . import Pool
def FetchAllStates(request):
    try:
        db, cmd = Pool.ConnectionPool()
        q = "select * from states"
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def FetchAllCities(request):
    try:
        db, cmd = Pool.ConnectionPool()
        stateid = request.GET['stateid']
        q = f"select * from cities where stateid={stateid}"
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)