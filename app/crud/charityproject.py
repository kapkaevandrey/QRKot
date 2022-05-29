from app.models.charityproject import CharityProject
from app.schemas.charityproject import ProjectCreate, ProjectUpdate
from app.crud.base import CRUDBase

project_crud = CRUDBase[CharityProject, ProjectCreate, ProjectUpdate](CharityProject)
