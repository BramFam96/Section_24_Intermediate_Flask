# Goals

Setting up our own apis: End points which accept and respond to json requests!

- Review HTTP Operations
- Introduction to REST

# TOC

[HTTP Operations](#get-v-post)  
[Introduction to Rest](#rest-intro)
[API Testing](#testing)

## Overview

---

- REST conceptually
- Build and Test JSON Apis

## HTTP OPERATIONS

## GET V POST

---

**GET** is used to _search/filter_

- Remains in history, can be bookmarked
- Data sent in URL
- Repeatable
  **Post** is used to trigger _update/send/ other side-effect_
- Does not cache or otherwise remain in history
- Data sent in request body

## PUT, PATCH, DELETE

---

HTML forms/links do not support **put**, **patch**, or **delete** -> why we haven't seen them  
Instead we would use these with AJAX or on the Server-side

- PUT
  - Update _entire_ resource
    - Entire post, comment, message board update;
- PATCH
  - Update _part_ of a resource (patch it up)
    - Date, username;
- DELETE
  - Self explainitory

## Safety and Idempotence

---

### **NOTE THESE ARE NOT ENFORCED! FOLLOW THE CONVENTION!**

Operations are considered **safe** if they do not change the data requested  
**Idempotent** operations can be performed repeatedly, and consecutively and return the same results

- In mathmatics this is an absolute operation;
  **GET** is the only **safe** HTTP operation  
  POST is the only **non-idempotent** HTTP operation

**NOTE DELETE is an idempotent operations, but the action of deleting will break this**

## Rest Intro

---

- REST is a design pattern that _defines constraints_ in the structure of web services (APIS)
  - Includes things like client-server model, statelessness, and cacheability
- APIS that _adhere_ to these contraints are considered **RESTful APIs**

### Why bother with this structure?

Example:  
Create an API route for updating a user.  
We could use any of the following:

- POST /users/[id]/update?
- POST /users/[id]/change?
- PATCH /users/[id]
  This flexibility creates the **need** to _standardize_

## Structure

---

Comprised of **operation**, **BASE_URL**, **resource**

```py
URL = 'http://api.site.com' || 'http://sit.com/api'
resource = f'{URL}/resource'
```

## RESTful routing conventions

---

| HTTP Verb | Route        | What it _should_ do |
| :-------- | :----------- | :------------------ |
| GET       | /snacks      | Get all snacks      |
| GET       | /snacks/[id] | Get snack           |
| POST      | /snacks      | Create snack        |
| PUT/PATCH | /snacks/[id] | Update snack        |
| DELETE    | /snacks/[id] | Delete snack        |

## RESTful Response Conventions

---

- **GET/snacks**
  - Should return 200 OK, JSON describing snacks
- **GET/snacks/[id]**
  - Should return 200 OK, JSON describing single snack
- **POST/snacks**
  - Should return 201 CREATED, JSON describing new snack
- **PUT or PATCH /snacks[id]**
  - Should return 200 OK, JSON describing updated snack

## Nested Routes

```py
/resource/[id]/comments/[comment_id]
```

Don't nest more than two resources in a single route

```py
/r/[cat_id]/posts/[p_id]/comments/[c_id]
# NOTE posts are already associated with cat:
# Instead use:
posts/[p_id]/comments/[c_id]
```

## Testing

---

We'll be testing JSON responses, not html  
We look for response.json -> easier!
[Test example](../flask-rest-json-api-demo/tests.py)

## Front-end considerations

---

- [JS](../flask-rest-json-api-demo/VideoCode/TodoAPI/static/todos.js)
- [HTML](../flask-rest-json-api-demo/VideoCode/TodoAPI/templates/index.html)  
  Delete requests will often originate on the client-side (delete button/action)  
  These requests are sent straight to api, and reflected in dom manipulation (different workflow)  
  In HTML:

```html
<ul>
	{%for todo in todos%}
	<li>
		{{todo.title}}
		<!-- data- tag is critical for Front-end to track id -->
		<button data-id="{{todo.id}}">X</button>
    <!-- Embed button in li to make it easier to delete -->
  </li>
	{% endfor %}
</ul>
```

Our HTML also _imports_ **bootstrap, jQuery, and AJAX**

```JS
$('.delete-todo').click(function() {
  const id = $(this).data('id');
  alert(id)
})
```

If written correctly, code abv should issue an alert with the todo's id  
Let's reformat it a bit:

```JS
$('delete-todo').click(deleteTodo);

async function deleteTodo() {
  // this refers to the button!
  const id = $(this).data('id')
  // We're not in python anymore! backticks not f strings
  await axios.delete(`/api/todos/${id}`)
  // Now we need to update the page
  $(this).parent().remove()
  console.log(`Deleted todo ${id}`
  ) 
}
```
