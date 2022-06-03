from app.models import CharityProject
from app.schemas.charity_project import ProjectCreate, ProjectUpdate
from app.crud.base import BaseCRUD


project_crud = BaseCRUD[CharityProject, ProjectCreate, ProjectUpdate](CharityProject)
