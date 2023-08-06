# 📦📦 pplmyapi (Python PPL myAPI wrapper) 
Czech PPL (Professional Parcel Logistic) API wrapper written in Python. Helps you to communicate with PPL myAPI without worring about fetching access tokens and constructing your own requests. All (hopefully) done for you in the background.

# Install it from PyPI
```bash
pip install pplmyapi
```

## Usage
This is still a work in progress, so the API might change in the future. However, the basic usage is as follows:
1. Create a `PPL` instance with your credentials
2. obtain a `RESTConnector` instance from the `PPL` instance.
3. use the `RESTConnector` instance to communicate with the PPL REST API (myAPI2)

### Send a package
```python
# Create Package instance with all the required data and 6 packages in the set
package = Package(
    reference_id="123456789",
    package_product_type=Product.PPL_PARCEL_CZ_PRIVATE_COD,
    note = "test",
    recipient=Recipient(
        name="John Doe",
        city="Hradec Králové",
        street="Hlavní 1",
        zip_code="50001",
        phone="123456789",
        email="j.doe@example.com",
        country = 'CZ'
    ),
    sender=Sender(
        name="Test s.r.o.",
        street="Testovací 55/36",
        city="Praha",
        zip_code="11000",
        country="CZ",
    ),
    payment_info=PaymentInfo(
        cod_price=100,
        cod_currency='CZK',
        cod_vs='123456789',
        insurance_price=100,
        insurance_currency='CZK',
        specific_symbol='123456',
        bank_account='123456789',
        bank_code='0300'
    ),
    weighted_package_info=WeightedPackageInfo(
        weight=10.22,
    ),
    package_set=(
        PackageSet(
            total_packages = 6,
        )
    ),
    flags=[
        PackageFlag(
            code=Flag.CL,
            value=True
        )
    ],
)
# create packages
packages = [package]

# create rest_connector
rest_con = ppl.connector()

# create rest_action
response = rest_con.post_shipments(
    packages=packages,
    file_path = './out_test',
    file_name = 'test_010223.pdf',
)
```
Response from the API is a dictionary containing the following keys:
- `labels`: base64 encoded labels from the API (all together)
- `packages`: list of `Package` instances (initionaly passed to the `post_shipments` function) with extended `shipment_number` attribute, `label_base64` attribute (with single label) and extended `package_set` attribute (with `related_packages` attribute containing list of `Package` instances related to the current package with the same `reference_id` attribute but different `shipment_number` attribute)  

### Get label for a package
```python
# TODO
```


## Development
If you're keen on contributing to this project, you can do so by forking this repository and creating a pull request. Please make sure to follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.