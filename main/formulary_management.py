from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from main.background_tasks import check_admin_permission

from main.csvio.added_inventory import AddedInventoryHandler
from main.csvio.initial_inventory import InitialInventoryHandler
from main.forms import (
    AddSupplyForm,
    CSVUploadForm,
    InventoryEntryForm,
    RemoveSupplyForm,
)
from main.models import Campaign, InventoryEntry


def formulary_home_view(request):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            campaign = Campaign.objects.get(name=request.session["campaign"])
            formulary = campaign.inventory.entries.all().order_by("medication")
            return_response = render(
                request,
                "formulary/home.html",
                {"page_name": "Inventory", "list_view": formulary},
            )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def add_supply_view(request):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            if request.method == "GET":
                form = InventoryEntryForm()
            else:
                form = InventoryEntryForm(request.POST)
                entry = form.save()
                entry.save()
            return_response = render(
                request, "formulary/add_supply.html", {"form": form}
            )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def edit_add_supply_view(request, entry_id=None):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            inventory_entry = InventoryEntry.objects.get(pk=entry_id)
            if request.method == "GET":
                form = AddSupplyForm()
                return_response = render(
                    request,
                    "formulary/edit_add_supply.html",
                    {
                        "page_name": inventory_entry,
                        "form": form,
                        "item_id": inventory_entry.id,
                    },
                )
            elif request.method == "POST":
                form = AddSupplyForm(request.POST)
                if form.is_valid():
                    inventory_entry.initial_quantity += int(request.POST["quantity"])
                    inventory_entry.quantity += int(request.POST["quantity"])
                    inventory_entry.save()
                    return_response = redirect("main:formulary_home_view")
                else:
                    return_response = render(
                        request,
                        "formulary/edit_add_supply.html",
                        {
                            "page_name": inventory_entry,
                            "form": form,
                            "item_id": inventory_entry.id,
                        },
                    )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def edit_sub_supply_view(request, entry_id=None):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            inventory_entry = InventoryEntry.objects.get(pk=entry_id)
            if request.method == "GET":
                form = RemoveSupplyForm()
                return_response = render(
                    request,
                    "formulary/edit_sub_supply.html",
                    {
                        "page_name": inventory_entry,
                        "form": form,
                        "item_id": inventory_entry.id,
                    },
                )
            elif request.method == "POST":
                form = AddSupplyForm(request.POST)
                if form.is_valid():
                    if inventory_entry.initial_quantity > int(
                        request.POST["quantity"]
                    ) and inventory_entry.quantity > int(request.POST["quantity"]):
                        inventory_entry.initial_quantity -= int(
                            request.POST["quantity"]
                        )
                        inventory_entry.quantity -= int(request.POST["quantity"])
                    else:
                        inventory_entry.initial_quantity = 0
                        inventory_entry.quantity = 0
                    inventory_entry.save()
                    return_response = redirect("main:formulary_home_view")
                else:
                    return_response = render(
                        request,
                        "formulary/edit_add_supply.html",
                        {
                            "page_name": inventory_entry,
                            "form": form,
                            "item_id": inventory_entry.id,
                        },
                    )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def csv_handler_view(request):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            return_response = render(
                request, "formulary/csv_handler.html", {"form": CSVUploadForm()}
            )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def csv_import_view(request):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            campaign = Campaign.objects.get(name=request.session["campaign"])
            form = CSVUploadForm(request.POST, request.FILES)
            result = ""
            if form.is_valid():
                upload = form.save()
                upload.save()

                if upload.mode_option == "1":
                    InitialInventoryHandler().read(upload, campaign)
                elif upload.mode_option == "2":
                    AddedInventoryHandler().read(upload, campaign)
                upload.document.delete()
                upload.delete()
                return_response = render(
                    request,
                    "formulary/csv_import.html",
                    {"result": "Formulary uploaded successfully."},
                )
            else:
                return_response = render(
                    request,
                    "formulary/csv_handler.html",
                    {"form": form, "result": result},
                )
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response


def csv_export_view(request):
    if request.user.is_authenticated:
        if check_admin_permission(request.user):
            campaign = Campaign.objects.get(name=request.session["campaign"])
            formulary = campaign.inventory.entries.all().order_by("medication")
            return_response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="formulary.csv"'},
            )
            handler = InitialInventoryHandler()
            return_response = handler.write(return_response, formulary)
        else:
            return_response = redirect("main:permission_denied")
    else:
        return_response = redirect("main:not_logged_in")
    return return_response
