class IAMController:
    def __init__(self, iam_service):
        self.iam_service = iam_service

    def get_iam_users_with_old_keys(self, age_in_hours):
        old_users = self.iam_service.get_iam_users_with_old_keys(age_in_hours)
        return {
            "users": old_users
        }

    def get_iam_users_with_unused_keys(self, days_unused):
        unused_users = self.iam_service.get_iam_users_with_unused_keys(days_unused)
        return {
            "users": unused_users
        }

    def handle_request(self, request):
        n_hours = request.get('n_hours')
        if n_hours is None:
            return {"error": "Parameter N is required"}, 400
        
        old_keys = self.get_old_access_keys(n_hours)
        return {"old_keys": old_keys}, 200
