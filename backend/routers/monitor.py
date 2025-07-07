from fastapi import APIRouter, HTTPException, Depends
from typing import List
from backend_py.schemas.monitor import MonitorCreate, MonitorUpdate, MonitorOut
from backend_py.repositories.monitor_repository import MonitorRepository
from backend_py.routers.user import get_current_user

router = APIRouter(prefix="/monitors", tags=["monitors"])

@router.post("/", response_model=MonitorOut)
async def create_monitor(monitor: MonitorCreate, current_user=Depends(get_current_user)):
    monitor_id = await MonitorRepository.create(monitor)
    created = await MonitorRepository.find_by_id(monitor_id)
    return created

@router.get("/", response_model=List[MonitorOut])
async def list_monitors(current_user=Depends(get_current_user)):
    # Assume organization_id is available on user
    return await MonitorRepository.find_by_organization(current_user.organization_id)

@router.get("/{monitor_id}", response_model=MonitorOut)
async def get_monitor(monitor_id: str, current_user=Depends(get_current_user)):
    monitor = await MonitorRepository.find_by_id(monitor_id)
    if not monitor or monitor.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor

@router.put("/{monitor_id}", response_model=MonitorOut)
async def update_monitor(monitor_id: str, updates: MonitorUpdate, current_user=Depends(get_current_user)):
    monitor = await MonitorRepository.find_by_id(monitor_id)
    if not monitor or monitor.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Monitor not found")
    await MonitorRepository.update(monitor_id, updates.dict(exclude_unset=True))
    updated = await MonitorRepository.find_by_id(monitor_id)
    return updated

@router.delete("/{monitor_id}")
async def delete_monitor(monitor_id: str, current_user=Depends(get_current_user)):
    monitor = await MonitorRepository.find_by_id(monitor_id)
    if not monitor or monitor.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Monitor not found")
    await MonitorRepository.delete(monitor_id)
    return {"message": "Monitor deleted"}

@router.post("/{monitor_id}/pause")
async def pause_monitor(monitor_id: str, current_user=Depends(get_current_user)):
    monitor = await MonitorRepository.find_by_id(monitor_id)
    if not monitor or monitor.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Monitor not found")
    await MonitorRepository.update(monitor_id, {"is_active": False})
    return {"message": "Monitor paused"}

@router.post("/{monitor_id}/resume")
async def resume_monitor(monitor_id: str, current_user=Depends(get_current_user)):
    monitor = await MonitorRepository.find_by_id(monitor_id)
    if not monitor or monitor.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Monitor not found")
    await MonitorRepository.update(monitor_id, {"is_active": True})
    return {"message": "Monitor resumed"}
