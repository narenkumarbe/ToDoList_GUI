import gooeypie as gp
import sqlite3

# Create a database or connect to one
conn = sqlite3.connect('mylist.db')
# Create a cursor
c = conn.cursor()
# Create a table
c.execute('''CREATE TABLE if not exists todo_list(list_item text)''')
conn.commit()
conn.close()

def add_new_task(event):
    # Adds a new task to the todo list when Enter Key is pressed
    if event.key['name'] == 'Return' and new_task_inp.text != '':
        todo_lst.add_item(new_task_inp.text)
        new_task_inp.clear()

def move_task(event):
    # Move a task from one listbox to another
    if event.widget == todo_lst:
        # move the task from the todo list to the done list
        done_lst.add_item(todo_lst.remove_selected())
    else:
        # move the task from done list to the todo list
        todo_lst.add_item(done_lst.remove_selected())

def delete_task(event):
    todo_lst.remove_selected()

def all_done(event):
    done_lst.items = done_lst.items + todo_lst.items
    todo_lst.items = []

def save_db(event):
    conn = sqlite3.connect('mylist.db')
    c = conn.cursor()
    c.execute('DELETE FROM todo_list;',)
    items = []    
    for item in todo_lst.items:
        c.execute("INSERT INTO todo_list VALUES(:item)",
        {
            'item': item,
        })        
    conn.commit()
    conn.close()
    app.alert('Information', 'Records added successfully','info')
      

def clear_task(event):
    done_lst.items = []

def main():
    conn = sqlite3.connect('mylist.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todo_list")
    records = c.fetchall()
    conn.commit()
    conn.close()
    for record in records:
        todo_lst.add_item(str(record[0]))
        #print(record)

app = gp.GooeyPieApp('Simple ToDoList')
app.width = 400

# Create all widgets
new_task_lbl = gp.Label(app, 'New Task')
new_task_inp = gp.Input(app)
todo_lbl = gp.Label(app, 'ToDo List')
todo_lst = gp.Listbox(app)
delete_task_btn = gp.Button(app, 'Delete Task', delete_task)
all_done_btn = gp.Button(app, 'All Done!', all_done)
done_lbl = gp.Label(app, 'Done!')
done_lst = gp.Listbox(app)
save_db_btn = gp.Button(app, 'Save to Database', save_db)
clear_all_btn = gp.Button(app, 'Clear All', clear_task)

#Event Listeners
new_task_inp.add_event_listener('key_press', add_new_task)
todo_lst.add_event_listener('double_click', move_task)
done_lst.add_event_listener('double_click', move_task)

# Add widgets to window
app.set_grid(5,3)
app.set_row_weights(0, 1, 0, 1, 0)
app.set_column_weights(0, 1, 1)
app.add(new_task_lbl, 1, 1, align='right')
app.add(new_task_inp, 1, 2, column_span=2, fill = True)
app.add(todo_lbl, 2, 1, align='right')
app.add(todo_lst, 2, 2, column_span=2, fill = True, stretch=True)
app.add(delete_task_btn, 3, 2, fill = True)
app.add(all_done_btn, 3, 3, fill = True)
app.add(done_lbl, 4, 1, align='right')
app.add(done_lst, 4, 2, column_span=2, fill = True, stretch=True)
app.add(save_db_btn, 5, 2, fill = True)
app.add(clear_all_btn, 5, 3, fill = True)

main()

new_task_inp.focus()
app.run()

