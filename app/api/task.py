from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, security, cruds
from app.api.dependencies import get_db

task_router = APIRouter()


@task_router.get("/", response_model=List[schemas.Task])
def get_task(
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get task.
    """

    tasks = cruds.get_tasks(db=db, owner_id=user.id)
    return tasks


@task_router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.CreateTask,
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create new task.
    """

    created_task = cruds.create_tesk(db=db, owner_id=user.id, task=task)

    return created_task


@task_router.post("/share")
def share_task(
    shared_with_email: schemas.CreateSharedTask,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """
    Share task.
    """
    if current_user.email == shared_with_email.shared_with_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't share task with yourself",
        )
    shared_with_id = cruds.get_user_by_email(db, shared_with_email.shared_with_email)
    if shared_with_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )
    created_shared_task = cruds.create_shared_task(
        db=db, owner_id=current_user.id, shared_with_id=shared_with_id.id
    )

    return created_shared_task


@task_router.get("/shared", response_model=List[schemas.Task])
def get_shared_task(
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get shared task.
    """
    tasks = cruds.get_shared_tasks(db=db, user_id=user.id)
    return tasks


@task_router.delete("/revoke-share")
def revoke_sharing(
    shared_with_email: schemas.CreateSharedTask,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """
    Remove shared task.
    """
    shared_with_id = cruds.get_user_by_email(db, shared_with_email.shared_with_email)
    if shared_with_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )
    try:
        cruds.delete_shared_task(
            db=db, owner_id=current_user.id, shared_with_id=shared_with_id.id
        )
    except (HTTPException, Exception) as e:
        raise e
    return


@task_router.patch("/reorder", response_model=List[schemas.Task])
async def update_order(
    order: int,
    task: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    """
    Update the order of a task.
    """
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task, models.Task.owner_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    try:
        user_tasks = cruds.update_task_order(db, db_task, order, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return user_tasks


@task_router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.UpdateTask,
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update task.
    """
    try:
        updated_task = cruds.update_tesk(
            db=db, task=task, task_id=task_id, owner_id=user.id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return updated_task


@task_router.delete("/{task_id}")
def delete_task(
    task_id: int,
    user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete task.
    """
    try:
        cruds.delete_task(db=db, task_id=task_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    return
