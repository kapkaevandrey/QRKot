from app.models.charity_project import CharityProject
from app.schemas.charityproject import ProjectCreate, ProjectUpdate
from app.crud.base import BaseCRUD


project_crud = BaseCRUD[CharityProject, ProjectCreate, ProjectUpdate](CharityProject)
