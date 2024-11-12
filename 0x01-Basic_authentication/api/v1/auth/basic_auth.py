from typing import TypeVar
from models.user import User  # Assuming User is defined in models.user


class BasicAuth(Auth):
    """Basic authentication class."""
    
    def decode_base64_authorization_header(self, base64_authorization: str) -> str:
        """Decodes a base64-encoded authorization header."""
        if not isinstance(base64_authorization, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization, validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user email and password from the decoded Base64 string."""
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> 'User':
        """Retrieves the User instance based on email and password."""
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # Search for user by email
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        # If user is found, validate password
        if len(users) == 0:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> 'User':
        """Overloaded method to get the current user based on the Authorization header."""
        if request is None:
            return None

        # Get the Authorization header
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None

        # Ensure the header starts with "Basic "
        if not authorization_header.startswith("Basic "):
            return None

        # Extract the Base64 part of the header
        base64_part = self.extract_base64_authorization_header(authorization_header[6:])
        if not base64_part:
            return None

        # Decode the Base64 part
        decoded = self.decode_base64_authorization_header(base64_part)
        if not decoded:
            return None

        # Extract the email and password from the decoded string
        email, password = self.extract_user_credentials(decoded)
        if email is None or password is None:
            return None

        # Retrieve the user object based on the credentials
        return self.user_object_from_credentials(email, password)
