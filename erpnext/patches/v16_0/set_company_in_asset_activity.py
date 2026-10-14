import frappe
import json

def execute():
    # Fill company from existing assets
    frappe.db.sql("""
        UPDATE `tabAsset Activity` aa
        JOIN `tabAsset` a ON aa.asset = a.name
        SET aa.company = a.company
        WHERE IFNULL(aa.company, '') = ''
    """)

    # Fill company for deleted assets from Deleted Document
    deleted_assets = frappe.get_all("Deleted Document",
        filters={"deleted_doctype": "Asset"},
        fields=["deleted_name", "data"]
    )

    for doc in deleted_assets:
        try:
            data = json.loads(doc.data)
            company = data.get("company")
            if company:
                frappe.db.sql("""
                    UPDATE `tabAsset Activity`
                    SET company = %s
                    WHERE asset = %s AND IFNULL(company, '') = ''
                """, (company, doc.deleted_name))
        except Exception:
            continue