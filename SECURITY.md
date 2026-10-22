# Security Policy

## Supported versions

Security fixes are made on the branch `19.0` and released as a new version `19.0.x.y.z`
of the affected modules. Older versions are not maintained.

| Branch | Supported |
| ------ | --------- |
| 19.0   | yes       |

## Reporting a vulnerability

Please do not report security problems in public issues, pull requests or discussions.

- Preferably use the private vulnerability reporting of GitHub: tab _Security_, _Report
  a vulnerability_ in
  [BM1-de/odoo-papierkram-import](https://github.com/BM1-de/odoo-papierkram-import/security).
- Or write an e-mail to the maintainer, Phillip Baumgärtner <baumgaertner@bm1.de>, with
  the subject "Security odoo-papierkram-import".

Describe the problem, the affected module and version, how to reproduce it and its
possible impact. Do not send real tax or personal data; use synthetic data for the
example.

We confirm the receipt, examine the report, keep you informed and publish a fix together
with a security notice in the changelog (`HISTORY.md` of the module). We credit you
unless you prefer not to be named.

## Scope

In scope are the modules of this repository, in particular:

- access of a user to data of a business (company) the user is not allowed to see, also
  through an import, its log and its attachments;
- injection through the uploaded files (Papierkram exports as ZIP, CSV and PDF files,
  category list, asset list, voucher splits and time entries), for example paths in a
  ZIP file that point outside of it.

Out of scope are vulnerabilities of Odoo itself or of other modules (please report them
to their maintainers) and wrong import results without a security impact (please open a
normal issue, without real data).

## Note

The modules only read the uploaded files and send no data anywhere. They are provided
free of charge and without warranty under the GNU AGPL-3.0 (see `LICENSE`).
