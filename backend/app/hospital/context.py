# hospital/context.py
from contextvars import ContextVar
from typing import Optional

# Context variable to store the current tenant ID
tenant_context: ContextVar[Optional[str]] = ContextVar('tenant_id', default=None)

def get_current_tenant_id() -> Optional[str]:
    """
    Get the current tenant ID from the context
    """
    return tenant_context.get()

def set_tenant_context(tenant_id: str) -> None:
    """
    Set the tenant ID in the current context
    """
    tenant_context.set(tenant_id)

def clear_tenant_context() -> None:
    """
    Clear the tenant ID from the current context
    """
    tenant_context.set(None)