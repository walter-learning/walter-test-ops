# Sales Ops Engineer - Technical test

## Initial setup

After cloning the repo, create a new file `.env` from `.env.dist` and fills in the 
variable using the values you were provided with.

Then, ensure you have Docker up and running and run the following command to build and test 
the lambda environnement :

```bash
sh run.sh -q 0 -b
```

If you get this output in your terminal :

```
🧰  Handler : handle
🌍  Invoked by web : False
📫  Event :
{}
👋 Hello, World!
✅  Lambda successfully executed :
{}
```

It means you are up and ready !

## [OPTIONAL] Dev dependencies

To enable autocompletion, we recommand to install dependencies in a virtual environnement :

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Questions

For each question, the corresponding handler can be found at `handlers/question_#.py` and the event at `events/event_#.json`

To run the handler of a question, use the following command :

```bash
sh run.sh -q X
```

For some question you will be told to use specific question number, for example `2.1`

### Q1. Some python manipulations

### Introduction

Please open `handlers/question_1.py`

`contacts_campaignA` and `contacts_campaignB` are two lists of `libs.clients.voice.models.Contact` instances retrieve from our database and defined by the following schema :

```python
class Contact(BaseModel):
    id: str | None = None  # Id of the contact
    campaign_id: str | None = None  # Id of the campaign
    phone: str | None = None  # Phone number of the contact
    retryDate: datetime | None = None  # Force the date of the next call
    lastCallAt: datetime | None = None  # Date of the last call
    assignedAgent: str | None = None  # Id of the agent assigned to the contact
    wrapup: str | None = None  # Wrapup of the contact
    totalCalls: int | None = None  # Total number of calls
    crm_id: str | None = None  # Id of the contact in the CRM

```

As written in their name, the first list comes from the campaign A and the second one from the campaign B.

A campaign is just a listing of phone number that are fed into the call engine of our provider that automatically 
call and transmit to our agent.

We suspect the presence of duplicates between the two campaigns...

#### Q1.1 : Build the list of phone numbers that are present in both campaigns

#### Q1.2 : Return the last time each duplicates was called in the two campaigns

The output should respect the following format :
```
+33620922865 
        A: 2025-03-23 06:30:05 
        B: 2025-03-28 04:47:45
+33650333176 
        A: N/A 
        B: 2025-03-10 23:14:12
...
```


## Q2. Post call handler

### Introduction

Please open `handlers/question_2.py`

This lambda is called by a webhook from our call provider that is triggered at the end of each call.

The webhook has the following payload, automatically converted to a Python object by the decorator `@lambda_handler` using the following model:

```python
class Event(BaseEvent):
    agent: str | None = None  # Username of the agent that handled the call
    callDurationInSeconds: str | None = None  # the entire call duration
    callBackDate: str | None = None # an optional date set by the agent to request a new call on a given date
    callEnd: str | None = None # when the call did end
    callId: str | None = None # the id of the call
    callResult: str | None = None # the result of the call from the phone system perspective
    callStart: str | None = None # when the call did start
    callType: str | None = None # the type of call (outbound or inbound)
    campaignId: str | None = None # the identifier of the campaign of which the contact is a part
    campaignName: str | None = None # the name of the campaign
    contactId: str | None = None # the id of the contact called
    contactPhone: str | None = None # the phone number of the contact called
    conversationDuration: str | None = None # the duration of the conversation (excluded ringing or SVI time)
    displayedPhoneNumber: str | None = None # the phone number of the agent 
    wrapup: str | None = None # the label the agent set to describe this call
    wrapupComment: str | None = None # an optionnal comment from the agent
```

#### Q2.1 : Schedule the next call

The first step of our post_call is to detect if the agent did request to schedule another call later
but with a twist: it is forbidden to plan a call for the same day so we have to ensure the callbackDate
is set at least for tomorrow.

A member from our team did implement this step before going on holydays but it doesn't seems to work at all...

Can you fix it ? We have setup a test event you can use using the following command :

```bash
sh run.sh -q 2.1
```

#### Q2.2 : Transfer to our support team

The second step to implement is to allow a transfer to our support team, more precissly to the support agent **with least numbers of contact** in the campaign B.
You can retrieve the list of agents from the CRM client and assign to agent by updating the contact after setting the `assignedAgent` property.

Again, a test event for this use case is available using the command : 

```bash
sh run.sh -q 2.2
```

## Q3. Time for some SQL

### Introduction

Please open `handlers/question_3.py`

This lambda is already connected to a SQLite database, its schema is available at `data/schema.png`.

An example is available on line 20 to understand how to send a query and retrieve the response from the database.

```python
cursor = db.cursor()
cursor.execute("SELECT * FROM session WHERE starting_date > ?", (date,))
data = cursor.fetchall()
cursor.close()
```

You can test it using the command

```bash
sh run.sh -q 3.0
```

#### Q3.1 : Sales from each team

Our sales ops teams needs some insights to complete its reporting, they need the number of sales
from each team as well as the amount, group by status to identify the number of unsubscription.

To test your implementation, use the following command :

```bash
sh run.sh -q 3.1
```


#### Q3.2 : Sales progression over the month

To help our sales managers, we were asked to create a tool that displays an agent's progress toward
their goal from day to day over a month. Our frontend developer has started to integrate this new 
module, but he needs the data in the following format:
```json
[
    {
        "date": "2025-04-01",
        "target_of_the_day": 1450,
        "amount_of_the_day": 2097,
        "progression_of_the_day": 1.45,
        "target_accumulated": 1450,
        "amount_accumulated": 2097,
        "progression_accumulated": 1.45,
    },
    {
        "date": "2025-04-02",
        "target_of_the_day": 1450,
        "amount_of_the_day": -699,
        "progression_of_the_day": 0,
        "target_accumulated": 2900,
        "amount_accumulated": 1398,
        "progression_accumulated": 0.48,
    },
    ...
]
```

To test your implementation, use the following command :

```bash
sh run.sh -q 3.2
```
