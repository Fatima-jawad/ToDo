from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List
from fastapi import HTTPException, status


from app import models, schemas, security


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def update_task_order(
    db: Session, task: models.Task, new_order: int, user_id: int
) -> List[models.Task]:
    conflicting_task = (
        db.query(models.Task)
        .filter(and_(models.Task.owner_id == user_id, models.Task.order == new_order))
        .first()
    )

    if conflicting_task and conflicting_task.id != task.id:
        db.query(models.Task).filter(
            and_(models.Task.owner_id == user_id, models.Task.order >= new_order)
        ).update({"order": models.Task.order + 1}, synchronize_session=False)

    task.order = new_order
    db.commit()

    # Return the refreshed list of tasks
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == user_id)
        .order_by(models.Task.order, models.Task.created_at)
        .all()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, owner_id: int) -> List[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)
        .order_by(models.Task.order, models.Task.created_at)
        .all()
    )


def create_tesk(db: Session, owner_id: int, task: schemas.CreateTask):
    last_order = (
        db.query(models.Task)
        .filter(models.Task.owner_id == owner_id)
        .order_by(desc(models.Task.order))
        .first()
    )
    last_order = last_order.order if last_order else 0
    db_obj = models.Task(
        title=task.title,
        description=task.description,
        order=last_order + 1,
        owner_id=owner_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_tesk(db: Session, task_id: int, task: schemas.UpdateTask, owner_id:int):
    db_obj = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == owner_id).first()
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db_obj.title = task.title
    db_obj.description = task.description
    db_obj.order = task.order
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_task(db: Session, task_id: int):
    db_obj = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db.delete(db_obj)
    db.commit()
    return db_obj


def create_shared_task(db: Session, owner_id: int, shared_with_id: int):
    db_obj = models.SharedTask(owner_id=owner_id, shared_with_id=shared_with_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_shared_tasks(db: Session, user_id: int):
    shared_tasks_ids = (
        db.query(models.SharedTask)
        .filter(models.SharedTask.shared_with_id == user_id)
        .all()
    )
    owners_ids = [task.owner_id for task in shared_tasks_ids]
    shared_tasks = (
        db.query(models.Task).filter(models.Task.owner_id.in_(owners_ids)).all()
    )
    return shared_tasks


def delete_shared_task(db: Session, owner_id: int, shared_with_id: int):
    db_obj = (
        db.query(models.SharedTask)
        .filter(owner_id == owner_id, shared_with_id == shared_with_id)
        .first()
    )
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shared tasks with this email not found"
        )
    db.delete(db_obj)
    db.commit()
    return
