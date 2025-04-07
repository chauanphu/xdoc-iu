## ERD

### Entity
#### 1. Hospital / Tenant: `tenant`
- `id`: unique key
- `name`: customer name
- `product_key` (string, unique): activation product key

#### 2. Patient Profile (Secured): `patient_profile`
- `id`: unique patient key
- `name`: patient name
- `dob` (datetime) date of birth
- `gender` (enum): MALE, FEMALE, OTHER

#### 3. Diagnosis (Secured): `diagnosis`
- `id`: unique key
- `patient_id` (foreign): patient id
- `doctor_id` (foreign, optional): the doctor diagnosing. If it is empty, it means the patient self-diagnoses.
- `time` (datetime): time of diagnosis
- `prediction`
- `conf` (float, 0 to 1): confidence
- `explain` (string): Explain the features significance in natural-language text

#### Doctor: `doctor`
- `id`: unique id
- `name`: doctor name
- `hashed_account_id`: hospital / tenant that the entity belongs to
- `tenant_id`: string

#### Account: `account`
Accounts entity for authentication and Role-Based-Access-Control (RBAC)
- `id`: unique account_id
- `email`: username / email (unique)
- `hashed_password`: hashed password
- `role` (enum): DOCTOR, PATIENT

### Relations ship

- **Tenant - Doctor** (Mandatory One - Optional Many): Each doctor must belong to a hospital system
- **Tenant - Patient Profile** (Optinal One - Optional Many): Each patient can be standalone, or assigned to a hospital
- **Diagnosis - Patient Profile** (Optional Many - Mandatory One): Each patient can have multiple different diagnosis
- **Diagnosis - Doctor** (Optional Many - Optional Many): Different doctors can give different diagnosis
- **Account - Doctor** (Mandatory One - Mandatory One)
- **Account - Patient** (Mandatory One - Mandatory One)