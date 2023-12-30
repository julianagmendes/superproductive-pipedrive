# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

# class WebhookUser(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     hashed_password = models.CharField(max_length=128)  # Use a length suitable for your hash function

# def create_webhook_user(username):
#     # Auto-generate a unique password for the user
#     password = generate_random_password()

#     # Hash the password before saving it to the database
#     hashed_password = make_password(password)

#     # Save the user to the database
#     user = WebhookUser.objects.create(username=username, hashed_password=hashed_password)

#     return user, password

# def authenticate_webhook_user(username, provided_password):
#     try:
#         user = WebhookUser.objects.get(username=username)
#     except WebhookUser.DoesNotExist:
#         return None

#     # Compare the provided password with the stored hashed password
#     if check_password(provided_password, user.hashed_password):
#         return user
#     else:
#         return None

# # Example usage:
# user, password = create_webhook_user("user123")

# # Later, when handling an incoming request:
# authenticated_user = authenticate_webhook_user("user123", provided_password_from_request)
# if authenticated_user:
#     # Proceed with processing the webhook for the authenticated user
# else:
#     # Reject the request
