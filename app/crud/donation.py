from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from app.crud.base import CRUDBase


donation_crud = CRUDBase[
    Donation, DonationCreate, DonationUpdate
](Donation)
