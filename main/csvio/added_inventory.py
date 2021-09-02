import csv
from main.models import InventoryCategory, InventoryEntry, InventoryForm, Manufacturer, Medication
from main.csvio.csv_interface import CSVHandler


class AddedInventoryHandler(CSVHandler):
    def __init__(self) -> None:
        super().__init__()
    
    def read(self, upload, campaign):
        return super().read(upload, campaign)
    
    def write(self, response, formulary):
        return super().write(response, formulary)
    
    def __export(self, response, formulary):
        return super().__export(response, formulary)

    def __import(self, upload, campaign):
        with open(upload.document.url) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)
            for row in reader:
                campaign.inventory.entries.add(
                    InventoryEntry.objects.update_or_create(
                        category=InventoryCategory.objects.get_or_create(
                            name=row[0])[0],
                        medication=Medication.objects.get_or_create(
                            text=row[1])[0],
                        form=InventoryForm.objects.get_or_create(
                            name=row[2]),
                        strength=row[3],
                        count=row[4],
                        quantity=row[5],
                        initial_quantity=row[6],
                        item_number=row[7],
                        box_number=row[8],
                        expiration_date=row[9],
                        manufacturer=Manufacturer.objects.get_or_create(
                            name=row[10])[0]
                    )
                )