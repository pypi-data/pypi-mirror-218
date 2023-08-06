from fastapi import APIRouter

from output.models.contact_database import Contacts
from output.models.label_database import Labels
from output.models.site_database import SitesContacts, Sites

router = APIRouter(
    prefix="/annuaires",
    tags=["Annuaires"],
)


@router.get("/")
async def get_list_sites_contacts_labels():
    return {"Contacts": Contacts.get_all(), "Sites": Sites.get_all(), "Labels": Labels.get_all()}


@router.post("/contacts")
async def create_contact(data: dict):
    contact = Contacts()

    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.number = data["phone"]
    contact.mail = data["email"]
    contact.address = data["address"]
    contact.commentary = data["comment"]

    contact.create()


@router.put("/contacts")
async def edit_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]
    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.mail = data["mail"]
    contact.address = data["address"]
    contact.number = data["phone"]
    contact.commentary = data["comment"]

    contact.update()


@router.delete("/contacts")
async def supp_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]

    contact.delete()


@router.post("/sites")
async def create_sites(data: dict):
    site = Sites()

    if data["siteName"]:
        site.site_name = data["siteName"]
        site.create()


@router.delete("/sites")
async def supp_site(data: dict):
    site = Sites()

    site.id = data["id"]

    site.delete()


@router.put("/sites")
async def edit_site(data: dict):
    site = Sites()

    site.id = data["id"]
    site.site_name = data["siteName"]

    site.update()


@router.post("/sites/contacts")
async def add_contact_in_site(data: dict):
    site = Sites(id=data["siteId"])
    previous_contacts = [ids for ids in site.get_contacts_by_site_id().keys()]
    new_contacts = [ids.get("id") for ids in data["contactsList"]]
    contacts_to_add = [contact for contact in new_contacts if contact not in previous_contacts]
    contacts_to_remove = [contact for contact in previous_contacts if contact not in new_contacts]

    for contact_id in contacts_to_add:
        site_contact = SitesContacts(site_id=site.id)
        site_contact.contact_id = contact_id
        site_contact.link_contacts_sites()

    for contact_id in contacts_to_remove:
        SitesContacts.remove_link_between_contacts_sites(id_site=site.id, id_contact=contact_id)


@router.post("/contacts/sites")
async def add_site_in_contact(data: dict):
    contact = Contacts(id=data["contactId"])

    sites = [int(ids) for ids in data["sites"]]
    previous_sites = [ids for ids in contact.get_sites_by_contact_id().keys()]
    sites_to_add = [ids for ids in sites if ids not in previous_sites]
    sites_to_remove = [ids for ids in previous_sites if ids not in sites]

    if sites_to_add:
        for site_id in sites_to_add:
            site_contact = SitesContacts(site_id=site_id, contact_id=contact.id)
            site_contact.link_contacts_sites()

    if sites_to_remove:
        for site_id in sites_to_remove:
            SitesContacts.remove_link_between_contacts_sites(id_site=site_id, id_contact=contact.id)
