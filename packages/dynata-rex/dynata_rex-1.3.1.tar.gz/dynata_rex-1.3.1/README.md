# rex-sdk-python

Package for building and interacting with the Dynata Respondent Exchange (REX)

---

## Quickstart:

---

### _**Opportunity Registry**_

#### Instantiate a Registry Client

```py
from dynata_rex import OpportunityRegistry
registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')
```

#### List opportunity notifications from the registry

```py
opportunities = registry.receive_notifications()


# [Opportunity(id=1,...), Opportunity(id=2,...), Opportunity(id=1,...)]
```

#### Convert an opportunity to JSON

```py
opportunity_json = Opportunity.json()
```

#### Acknowledge a list of notifications from the registry

```py
registry.ack_notifications([opportunity_1.id, ..., opportunity_N.id])
```
#### Acknowledge a single notification from the registry
```
registry.ack_notification(opportunity.id)
```

#### Get a list of corresponding opportunities from a project_id

```py
corresponding = registry.list_project_opportunities(opportunity.project_id)

# [12345, 45678, 78901]
```

#### Download a collection from a collection-type targeting cell

```py
data = registry.download_collection(cell.collection_id)
```

---

### _**Respondent Gateway**_

#### Instantiate a RespondentGateway Client

```py
from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')
```

#### Create a survey link for your respondent

```py
url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'

signed_link = gateway.create_respondent_url(url,
                                            '1990-01-01',
                                            'male',
                                            '90210',
                                            'very-unique-respondent-id',

                                            ttl=60)
# https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&birth_date=1990-01-01&gender=male&postal_code=90210&respondent_id=very-unique-respondent-id&access_key=rex_access_key&expiration=2021-11-29T15:35:12.993Z&signature=4353e8c4ca8f8fb75530214ac78139b55ca3f090438c639476b8584afe1396e6
```

#### Add additional query parameters to a link that will be present on return from survey

```py
url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'

custom_params = {
    'custom_parameter': 'custom_value',
    'another_custom_parameter': 'another_custom_value'
}

signed_link = gateway.create_respondent_url(url,
                                            '1990-01-01',
                                            'male',
                                            '90210',
                                            'very-unique-respondent-id',
                                            additional_params=custom_params,
                                            ttl=60)

# https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&custom_parameter=custom_value&another_custom_parameter=another_custom_value&birth_date=1990-01-01&gender=male&postal_code=90210&respondent_id=very-unique-respondent-id&access_key=rex_access_key&expiration=2021-12-02T13:48:55.759Z&signature=cf443326b73fb8af14c590e18d79a970fc3f73327c2d140c324ee1ce3020d064
```

#### Sign an inbound /start link with your credentials

```py
url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'
signed_url = gateway.sign_url(url)

# "https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&access_key=rex_access_key&expiration=2021-11-24T16:12:06.070Z&signature=fa8b5cac82d34bcf8026904b353349db5b1b871f735e07a601389cb6da2d744d"
```

#### Generate a URL-quoted signed url

```py
signed_url = gateway.sign_url(url, url_quoting=True)

# 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&access_key=rex_access_key&expiration=2021-11-24T16%3A12%3A35.991Z&signature=4219cf63406ae429d94dbe9c33027816c264c1e2bf1edbadd2510eb9bf2351c3'
```

### Verify a signed /end link URL with your credentials

##### Valid URL

```py
# Termination Endlink
end_url = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"

gateway.verify_url(end_url)

# True
```

##### Missing Signature

```py
missing_signature = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z"

gateway.verify_url(missing_signature)

# False
```

##### Altered Parameters (Term --> Complete Attempt)

```py
# Disposition changed to 1 (from 2) and status to 0 (from 1)

altered_parameters = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=1&status=0&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"

gateway.verify_url(altered_parameters)

# False
```

##### Get Disposition of a Survey from Endlink

```py
termination = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"

disposition = gateway.get_respondent_disposition(termination)

# <GatewayDispositionsEnum.TERMINATION: 2>

disposition.name

# 'TERMINATION'

disposition.value

# 2
```

##### Get Disposition + Status of a Survey from Endlink

```py
termination = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"

status = gateway.get_respondent_status(termination)

#<GatewayStatusEnum.TERMINATION_DYNATA: (<GatewayDispositionsEnum.TERMINATION: 2>, 1)>

status.name

# 'TERMINATION_DYNATA'

status.value

# (<GatewayDispositionsEnum.TERMINATION: 2>, 1)
```

##### Create a context

```py
context_id = 'super-unique-ctx-id'
data = {
    'ctx': 'parent-context-id',           # From survey link 'ctx' parameter
    'gender': 'male',
    'birth_data': '1999-09-09',
    'postal_code': '90210'
}
gateway.create_context(context_id, data)

# 'super-unique-ctx-id'
```

##### Retrieve a context

```py
gateway.get_context('super-unique-ctx-id')

# {
#    'id': 'super-unique-ctx-id',
#    'items': {
#        'ctx': 'parent-context-id',
#        'gender': 'male',
#        'birth_data': '1999-09-09',
#        'postal_code': '90210'
#     }
# }
```

##### Expire a context

```py
gateway.expire_context('super-unique-ctx-id')

# {
#    'id': 'super-unique-ctx-id',
#    'items': {
#        'ctx': 'parent-context-id',
#        'gender': 'male',
#        'birth_data': '1999-09-09',
#        'postal_code': '90210'
#     },
#     'expiration': '2021-11-30T16:10:44Z'
# }
```

##### List Attributes

```py
gateway.list_attributes('country', 'page_number', 'page_size')

# {
#    'data':
#    [
#       {
#           'active': true,
#           'parameter_id": 402
#       }
#    ]
# }
```

##### Get Attribute Info

```py
gateway.get_attribute_info('attribute-id')

# {
#   'id': 402,
#   'name': "This Parameter",
#   'description': "Details of what this is",
#   'display_mode: "N" (Optional),
#   'parent_dependencies':
#   [
#       'answer_ids':
#       [
#           { 12 }
#       ],
#       'parameter_id':403
#   ],
#   'expiration_duration': 36000 (Optional),
#   'is_active': true,
#   'countries':
#   [
#       { "US" }
#   ],
#   'question': (Optional)
#   {
#       'text': "How much wood can a woodchuck?",
#       'translations':
#       [
#           {
#               'locale': "BG",
#               'text': "Other Language"
#           }
#       ]
#   }
#   'answers':
#   [
#       {
#           'id': 99,
#           'text': "A ton",
#           'countries':
#           [
#               { "US" }
#           ],
#           'translations':
#           [
#               {
#                   'locale': "GB",
#                   'text': "Other language"
#           ]
#       }
#   ]
# }
```

#### put respondent

```python
from dynata_rex.models import PutRespondentRequest, Attribute

respondent = PutRespondentRequest(
    respondent_id="respondent_id",
    gender="gender", # str | None
    country="country",
    language="language",
    birth_date="birth_date", # str | None
    attributes= [Attribute(attribute_id=111, answers=[111, 222, 333])],
    postal_code="postal_code" # str | None
)

gateway.put_respondent(respondent)
```

#### put respondent answers

```python
from dynata_rex.models import PutRespondentAnswersRequest, Attribute

respondent_answers = PutRespondentAnswersRequest(
    respondent_id="respondent_id",
    attributes= [Attribute(attribute_id=111, answers=[111, 222, 333])]
)

gateway.put_respondent_answers(respondent_answers)
```