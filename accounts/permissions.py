"""
Role-based permission classes for the Blood Bank Management System.

# BBMS-SR-002: Role-based access control enforced at the API layer.
"""

from rest_framework.permissions import BasePermission


class IsStaffOrAdmin(BasePermission):
    """
    Allow access only to users with the 'staff' or 'admin' role.
    Used for endpoints like POST /api/donations.
    """

    # BBMS-SR-002
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('staff', 'admin')
        )


class IsHospitalOrStaffOrAdmin(BasePermission):
    """
    Allow access to users with 'hospital', 'staff', or 'admin' role.
    Used for endpoints like GET /api/inventory and GET /api/inventory/search.
    """

    # BBMS-SR-002
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('hospital', 'staff', 'admin')
        )


class IsDonorOwnerOrStaffAdmin(BasePermission):
    """
    Donors can access their own data; Staff and Admin can access all data.
    Used for GET /api/donations/history.
    """

    # BBMS-SR-002
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
