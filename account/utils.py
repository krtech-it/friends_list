from .models import Case

class FriendRequiredMixin:
    def get_user_context(self, request, *args, **kwargs):
        if request.user.profile.friends.filter(id=kwargs['userID']).exists():
            return True
        else:
            return False

class CheckUserCaseMixin:
    def check_user_case(self, request, *args, **kwargs):
        try:
            case = Case.objects.get(id=self.kwargs.get('pk'))
        except:
            return False
        if request.user.profile.id == case.profile.id:
            return True
        else:
            return False

