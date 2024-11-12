from typing import List

class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether authentication is required for the given path.
        Returns True if the path is not in the excluded_paths list, 
        considering wildcard "*" at the end of the excluded paths.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Remove trailing slashes for slash tolerance
        path = path.rstrip("/")

        for excluded in excluded_paths:
            # Remove trailing slashes for slash tolerance on excluded paths
            excluded = excluded.rstrip("/")

            # Check for exact match
            if path == excluded:
                return False

            # Check for wildcard match (ends with *)
            if excluded.endswith("*"):
                # Remove the trailing '*' for comparison
                prefix = excluded[:-1]
                if path.startswith(prefix):
                    return False

        return True
