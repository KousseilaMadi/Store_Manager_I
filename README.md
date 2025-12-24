#### **Features:**
- scanning products and filling the database
- scanning a product to add it to the total and removing the products from the database once purchase is cofnirmed
- printing a receipt (list with prices and total + date)

### **Structure:**
- **Models:** define database models, attributes and properties
- **Respositories:** contain atomic database operations
- **Services:** uses the repos operations to create use case operations
- **UI:** made with PyWebView(html, css, js) to create interactive interface
- **API:** a set of wrapper functions that call services functions to create functions that are better to use in js, errors are handled in these wrapper functions to create a json opject report that js can read easily and convert fetched data from ORM object into json object so they can be read in js.
using the API leads to writing a little moe code but it keeps everything organized and centered in the backend so in js (frontend) you wont face issues handling errors or receiving unreadable data objects, it acts as an interpreter to the actions happening in the front end, while services make the modifications to the backend

### **Interface Pages:**
- **Splash:**
- **Login:**
- **Signup:**
- **Register:**
- **Sales(Admin Only):**
- **Stock(Admin Only):**
- **Account:**

each will have navigation bar if the page is AO (Admin Only) it will have a different nav bar that offers more than the regular user nav bar that offers less

### **State struct:**
state is a struct where some data is stored these data are crucial for the functioning of the app .

```json
{
    state: {
        current_register: <value>,
        max_register_number: <value>,
        registers:{
            <key>: <value>
            'register-id':[]
        },
        current_user:{
            <key>: <value>
        },
        filters:{
            <key>: <value>
            'page':{
                'filter_name':<value>
            }
        }
    }
}
```

### **Pages Features**:
### Splash: the first screen to show and it displays the studio name in large letters
### Login: allows to login to an account
### Signup: allows to create new accounts
### Register: 
- add products to cart by search
- add products to cart by scanning barcode
- add divers item if it s not something you have in stock
- create several registers
- checkout and save the sale
### Sales:
- see all sales and apply refunds
- see all refunds
- filter sales
- see stats of profit and revenue
### Stock:
- add products to stock
- edit existing products
- remove products from stock
### Account:
- change account password
- add new users
- change roles of existing users
- delete users accounts
- logout


### PS:
the project is well structured and coded so it s felxible for any addition of features or editing of existing ones

### Bugs:
- sales loading is functional but acts weird


### **Store Manager V1.0.0**