# hospital/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .context import set_tenant_context, clear_tenant_context
from auth.services import get_current_user
from db.mongo import get_database
from doctor.services import get_doctor_by_account_id
from patient.services import get_patient_by_account_id

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Clear tenant context before processing
        clear_tenant_context()
        
        try:
            # Extract tenant ID from header or token if available
            tenant_id = request.headers.get("X-Tenant-ID")
            
            # If tenant ID is not in headers, try to get it from the authenticated user
            if not tenant_id:
                try:
                    # Use auth utilities to get the current user (if authenticated)
                    user = await get_current_user(request)
                    if user:
                        # Get database
                        db = await get_database()
                        
                        # Check if user is a doctor and get tenant ID
                        doctor = await get_doctor_by_account_id(db, str(user.id))
                        if doctor and doctor.tenant_id:
                            tenant_id = doctor.tenant_id
                        
                        # If not a doctor, check if user is a patient with a tenant
                        if not tenant_id:
                            patient = await get_patient_by_account_id(db, str(user.id))
                            if patient and patient.tenant_id:
                                tenant_id = patient.tenant_id
                except Exception:
                    # If any errors occur during tenant detection, proceed without tenant context
                    pass
            
            # Set tenant context if we have a tenant ID
            if tenant_id:
                set_tenant_context(tenant_id)
                
            # Process the request
            response = await call_next(request)
            
            # Add tenant ID to response headers for debugging if needed
            if tenant_id:
                response.headers["X-Tenant-ID"] = tenant_id
                
            return response
            
        finally:
            # Always clear tenant context after request is processed
            clear_tenant_context()