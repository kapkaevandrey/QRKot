from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from app.crud.base import BaseCRUD


class DonationCRUD(BaseCRUD[Donation, DonationCreate, DonationUpdate]):
    pass


donation_crud = DonationCRUD(Donation)
