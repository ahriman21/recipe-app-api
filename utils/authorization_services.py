
@staticmethod
def is_owner(obj,request):
    if obj.user != request.user:
        return False
    return True