#coding:utf-8

from web import form
from utils.mongodb import get_col_handler
#from collections import get_categories


class regexp_(form.regexp):
    
    def valid(self, value):
        return bool(self.rexp.search(value))

vcontent = regexp_(ur'[\u4e00-\u9fa5]', 'Sorry, needs Chinese Words!')
vaddr = form.regexp(r'^http://(.+)$', 'Please input correct address!')
vemail = form.regexp(r'^\w+?@.+?$', 'Please input correct email address!')

cgform = form.Form(
    form.Textbox("name", form.notnull, description="Must input a name!"),
    form.Hidden("id", value=0),
    form.Button("submit", type="submit", description="Submit"),
    validators = [form.Validator("Name Existed or ID is Wrong!", lambda i:check_existed('category', \
{'name':i.name, 'id':i.id}))])

articalf = form.Form(
    form.Hidden("id", value=0),
    form.Textbox("title", form.notnull, description="Title"),
    form.Textbox("tags", value="", description="Tags"),
    form.Textbox("author", form.notnull, value="Chang.Jian", description="Author"),
#    form.Dropdown("category_id", 
#        args=map(lambda i:(i['id'], i['name']), get_col_handler('category').find()), 
#        description="Category"),
    form.Textarea("content", form.notnull, description="Content"),
    form.Button("submit", type="submit"),
)

linkform = form.Form(
    form.Hidden("id", value=0),
    form.Textbox("link_addr", vaddr, value="http://", description="Link address"),
    form.Textbox("link_name", form.notnull, description="Link name"),
    form.Textbox("friend_name", form.notnull, description="Friend name"),
    form.Textbox("description", description="Description"),
    form.Button("submit", type="submit")
)


class Checkbox(form.Checkbox):
    
    def get_value(self):
        return self.value        

commentf = form.Form(
    form.Hidden("id", value=0), 
    form.Hidden("artical_id", value=0),
    form.Hidden("comment_id", value=0),
    form.Textbox("name", form.notnull, description="Name*:"),
    form.Textbox("email", vemail, description="Email(Hidden)*:"),
    form.Textbox("website", value="http://",  description="Website"),
    form.Textarea("content", vcontent, description="Content*:"),
    form.Checkbox("remember_me", description="Remember Me", checked=True),
    form.Textbox("vname", form.notnull, description="Name again*:"),
    form.Button("Submit", type="submit"),
    validators = [form.Validator("Wrong in Name again", lambda i:i.name==i.vname)],
)

def check_existed(col, fields):
    if not isinstance(fields, dict):
        return False
    id = fields.pop('id', 0)
    status = 'add'
    if int(id) != 0:
        status = 'edit'
    col_handler = get_col_handler(col)
    if status == 'add':
        result = col_handler.find_one(fields)
        if result:
            return False
    else:
        fields.update({'id':{'$ne':int(id)}})
        result = col_handler.find_one(fields)
        if result:
            return False
    return True

