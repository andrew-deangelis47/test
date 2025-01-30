from mietrak_pro.models import User


def get_assigned_estimator_by_id(estimator_id: int):
    estimator = User.objects.filter(code=estimator_id).first()
    return estimator
