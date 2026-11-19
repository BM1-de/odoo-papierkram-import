## 20.0.1.0.0 (2026-11-19)

- Migration to Odoo 20.
- The permission of the import is in `security/ir.access.csv` now, with the
  same content as before.
- Binary fields return binary values instead of base64: the uploaded exports
  and lists are read and the PDF documents are attached that way.
- Odoo 20 regards a contact as a company only if it has a VAT number. A
  contact that Papierkram lists as a company (its name differs from the default
  recipient) and a contact known only by its name on a document stay companies
  without VAT number, as in 19.0: the import marks them with the new field
  _Company in Papierkram_ of the contact.
- The form of a finished import hides the files that were not uploaded;
  Odoo 20 would show "false" for them.
- The button of the imported entries uses an icon of Odoo 20 (Material
  Symbols).

## 19.0.1.0.0

- First version for Odoo 19: contacts, customer invoices, cancellations and
  credit notes, expense and income vouchers, payments with their own payment
  date, fixed assets with their depreciation and the original PDF documents
  from the yearly exports of Papierkram; the complete history or only the
  open items; contacts already present with the same name are used.
