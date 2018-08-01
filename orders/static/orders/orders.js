// Javascript for the index page

// #############  CLASSES  #############

class Order_line {
  constructor (line_id, category, item, item_price, size, toppings_opt, toppings_desc, toppings_list, sub_options_list, ttl_price) {
    //TODO: make these all null
    this.line_id = (new Date).getTime();
    this.category = category;
    this.item = item;
    this.item_price = item_price;
    this.size = size;
    this.toppings_opt = toppings_opt;
    this.toppings_desc = toppings_desc;
    this.toppings_list = toppings_list;
    this.sub_options_list = [];
    this.total_line_price = ttl_price;
  } //  end constructor
} //end CLASS ORDER_LINE


class Cart {
  constructor () {
    this.order_lines = new Array();
    this.order_total = 0;
  }

} // end CLASS CART

// #############  END CLASSES  #############

// #############  CART FUNCTIONS  #############

toppings_list_populated = false;
line_in_process = false;
order_in_process = false;

// load existing cart
if ( localStorage.getItem('stored_cart') ) {
  load_cart();
} else {
  localStorage.setItem('stored_cart', JSON.stringify(new Cart()));
}

function get_cart() {
  return JSON.parse(localStorage.getItem('stored_cart'));
}

function cart_new_line(cart) {
  cart.order_lines.push(new Order_line());
}

function cart_cur_line(cart) {
  return cart.order_lines[ cart.order_lines.length - 1 ];
}

function cart_get_line(line, cart) {
  return cart.order_lines[line];
}

function set_cart(cart) {
  localStorage.setItem('stored_cart', JSON.stringify(cart));
}

function cart_remove_line (line_id, cart) {
  for (line in cart.order_lines) {
    if (cart.order_lines[line].line_id == line_id){
      cart.order_lines.splice(line,1);
      cart_recalc_total(cart);
      set_cart(cart);
    }
    clear_cart_table();
    refresh_cart_table();
  }
} // end remove()

function clear_cart() {
  localStorage.setItem('stored_cart', JSON.stringify(new Cart()));
  clear_cart_table(); //clear the shopping cart display

  //update number of cart items in header
  document.getElementById('num_cartitems').innerHTML = "0 items";
}

function cart_recalc_total (cart) {
  cart.order_total = 0;
  for (var i in cart.order_lines) {
    cart.order_total += cart_get_line(i, cart).total_line_price;
  }
  //update number of cart items in header
  document.getElementById('num_cartitems').innerHTML = cart.order_lines.length;
  if (cart.order_lines.length == 0 ) {
    document.getElementById("cartinfo").hidden = true;
  }

} // end recalc_total()

// #############  END CART FUNCTIONS  #############


// ########################  begin DOMContentLoaded ########################
document.addEventListener('DOMContentLoaded', (evevnt) => {
  // wait till page loads before setting up javascript elements
  setup_order_modal();

});
// ########################  end DOMContentLoaded ########################

function setup_order_modal () {

  document.getElementById('menu_item_selection').onchange = refresh_modal;
  document.getElementById('size_selection').onchange = update_modal;

  document.getElementById('btn_add_to_cart').onclick = add_to_cart;
  document.getElementById('btn_place_order').onclick = place_order;

  document.getElementById('btn_close_success').onclick = () => {
    s_modal = document.getElementById('order_success_modal');
    s_modal.style.display="none";
  }

  document.getElementById('cancel_modal').onclick = () => {clear_modal();}

} // end setup_order_modal()


// send current cart to server
function place_order() {

  const place_order = new XMLHttpRequest();
  place_order.open('POST', '/place_order');
  place_order.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

  place_order.onload = () => {
    const message = JSON .parse(place_order.responseText)
    // after order is placed, clear the card and display succes modal
    clear_cart();
    display_order_success_modal(message);
    document.getElementById("cartinfo").hidden = true;
    order_in_process=false;
  } //end onload

  // Add data to send with request
  const data = new FormData();
  data.append('cart', JSON.stringify(cart));
  place_order.send(data); // Send request
  return false; // avoid sending the form

} // end place_order


// helpder function for place_order() -- populate success modal and display it
function display_order_success_modal(message) {
  o_number = document.getElementById('order_number')
  o_number.innerHTML = message["order_number"];

  o_total = document.getElementById('order_ttl')
  ttl = Number(message["order_total"]).toFixed(2)
  o_total.innerHTML = `$${ttl}`;

  $("#order_success_modal").modal();
}

function load_cart() {
  //add cart items to modal and update header line
  refresh_cart_table();
  cart_recalc_total(cart);
} // end load_cart()

// add current line items to cart
function add_to_cart() {
  // cart.add_cur_line();
  cart = get_cart();
  cart_recalc_total(cart);
  set_cart(cart);
  clear_modal();
  refresh_cart_table();
  if (!order_in_process) {
    order_in_process=true
    document.getElementById("cartinfo").hidden = false;
  };

  //put cart in local storage
  localStorage.setItem('stored_cart', JSON.stringify(cart))
  line_in_process = false;

} // end add to cart

//called to draw the line item modal when a new menu item was selected
function refresh_modal() {draw_modal(initial_modal);}

//called to draw the line item modal when a change was made to the line
//other than selecting a new menu item
function update_modal() {draw_modal(update_line_summary);}

// gets a menu item from the server based on user selections
// updates the modal based on the 'modal_function' argument
function draw_modal(modal_function) {

  if (line_in_process == false) {
    cart = get_cart();
    cart_new_line(cart);
    set_cart(cart);
    line_in_process = true;
  }

  const get_menu_items = new XMLHttpRequest();
  const sel_item = get_selected_menu_item().item;
  const sel_cat = get_selected_menu_item().category;
  const sel_size = get_selected_size();
  const sel_toppings_list = get_selected_pizza_toppings();
  const sel_subOptions = get_selected_subOptions();

  get_menu_items.open('POST', '/get_menu_items');
  get_menu_items.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

  get_menu_items.onload = () => {
    const response = JSON.parse(get_menu_items.responseText)
    modal_function(response);
  } //end onload

  // Add data to send with request
  const data = new FormData();

  data.append('sel_item', sel_item);
  data.append('sel_cat', sel_cat);
  data.append('sel_size', sel_size);
  data.append('sel_toppings_list', sel_toppings_list);
  data.append('sel_subOptions', sel_subOptions);

  get_menu_items.send(data); // Send request
  return false; // avoid sending the form

} // end func_get_items()


// starts modal from scratch - unless pizza type is the only thing that changed
// called when a new menu item is selected
function initial_modal(item) {

  document.querySelector('#size_selection').hidden = true;
  document.querySelector('#toppings_group').hidden = true;
  document.querySelector('#sub_options').hidden = true;

  // If item has size option, show size
  if (item.size != 'NA') {
    document.querySelector('#size_selection').hidden = false;
    document.getElementById('size_lg').checked = true; //large is default
  } else {
    document.getElementById('size_lg').checked = false;
    document.getElementById('size_sm').checked = false;
  }

  // if item is a Pizza, show the toppings selection
  if (item.category == 'Pizza' ) {
    if (!toppings_list_populated) { load_pizza_toppings() }
    document.querySelector('#toppings_group').hidden = false;
  } else { // otherwise, clear the toppings and hide them
    clear_toppings();
  }

  // if item is a Sub, show extra cheese option
  if (item.category == 'Sub' ) {
    clear_sub_options();
    load_sub_options(item);
    document.querySelector('#size_selection').hidden = false;
    document.querySelector('#sub_options').hidden = false;
  } else { // otherwise, clear the toppings and hide them
    clear_sub_options();
  }

  if (item.category == 'Dinner Platter') {
    document.querySelector('#size_selection').hidden = false;
  }

    update_line_summary(item);

} // end display_modal_options()

// called when a sub is selected - updates the modal to show addons available
function load_sub_options(item) {

  addons = item.addons;

  // loop through reponse items and add them to the dropdown
  for (a in addons){
    const check_box = document.createElement('input');
    check_box.type = "checkbox"
    check_box.name = "sub_option";
    check_box.value = a;

    var data = document.createAttribute("data-addon_price");
    data.value = addons[a];
    check_box.setAttributeNode(data);

    check_box.onchange = () => {update_modal()};

    const cb_text = document.createElement('span');
    cb_text.innerHTML = `${a} (\$${addons[a]})`;

    const br = document.createElement('br');

    sub_options = document.getElementById("sub_options");
    sub_options.appendChild(check_box);
    sub_options.appendChild( document.createTextNode( '\u00A0' ) );
    sub_options.appendChild(cb_text);
    sub_options.appendChild(br);
  }; // end for i in response loop

} // end load_sub_options


// called once to load the pizza toppings available
function load_pizza_toppings() {
  //initialize new request
  const get_toppings = new XMLHttpRequest();

  get_toppings.open('POST', '/get_toppings');
  get_toppings.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

  //when request is completed
  get_toppings.onload = () => {
    //extract JSON data from request
    const response = JSON.parse(get_toppings.responseText)
    // loop through reponse items and add them to the dropdown
    // add each item to id="toppings_list"
    for (t in response){

      const list_item = document.createElement('div');
      var list_item_data = document.createAttribute("data-topping");
      list_item_data.value = response[t];
      list_item.setAttributeNode(list_item_data);
      list_item.innerHTML = response[t];
      list_item.onclick = () => {
          // add to selected toppings list
          const topping = list_item.dataset.topping;
          const sel_item = document.createElement('div');
          sel_item.id = topping;
          sel_item.className = "selected_pizza_toppings";
          sel_item.innerHTML = topping;

          // append a remove topping button (- pill)
          const remove_but = document.createElement('span');
          remove_but.className = "badge badge-pill badge-danger ml-2";
          remove_but.innerHTML = "&times;";
          remove_but.onclick = () => {
            // code to remove item from the list
            this_item = document.getElementById(topping);
            this_item.parentNode.removeChild(this_item);
            list_item.hidden = false;
            update_modal();
          } // end remove button on click
          sel_item.appendChild(remove_but);

          // add selected item to list
          sel_toppings_list = document.getElementById("selected_toppings");
          sel_toppings_list.appendChild(sel_item);
          list_item.hidden = true;

          update_modal();
        } // end div_onclick

      toppings_list = document.getElementById("toppings_list");
      toppings_list.appendChild(list_item);

      }; // end for t in response loop

      toppings_list_populated = true;

    } // end onload

    // Send request
    get_toppings.send();
    return false; // avoid sending the form and creating an HTTP POST request

} // end load_pizza_toppings()

// returns the selected menu item from the modal window
function get_selected_menu_item () {
    var i = document.getElementById("menu_item_selection");
    i_text = i.options[i.selectedIndex].text;
    i_split = i_text.split(':');
    category = i_split[0];
    item = i_split[1].trim();
    return {"category":category, "item":item};
}

// get the selected size.  return LG if neither is selected
function get_selected_size() {
  size_radios = document.getElementsByClassName("selected_size")
  num_radios = size_radios.length;
  for (var i=0; i<num_radios; i++) {
    if (size_radios[i].checked) {
      return size_radios[i].value
    }
  }
  return "LG" //default
} // end get_selected_size()

//returns a list of pizza toppings selected by user
function get_selected_pizza_toppings() {
    elements = document.getElementsByClassName('selected_pizza_toppings');
    rv = []
    for (i=0; i<elements.length; i++) {
      rv.push(elements[i].id);
    }
    return rv;
} // end get_selected_pizza_toppings

//counts number of toppings selected by user
function count_selected_pizza_toppings() {
  elements = document.getElementsByClassName('selected_pizza_toppings');
  return elements.length;
} // end count_slected_pizza_toppings()

//returns a list of addons selected by the user
function get_selected_subOptions() {
    elements = document.getElementsByName("sub_option");
    rv = [];
    for (i=0; i<elements.length; i++) {
      if (elements[i].checked == true) {
        rv.push(elements[i].value);
      }
    }
    return rv;
} // end get_selected_subOptions()


// update the modals line item summary
function update_line_summary(item) {

  s_line = document.getElementById('item_display');

  if (item.category == "Pizza") {
    s_line.innerHTML = `${item.item} (${item.size}) // ${item.toppings_desc} // Price: ${item.price}`;

  } else if (item.category == "Sub") {

    total_line_price = Number(item.price);
    addons_text = '';

    item_text = `${item.category}:${item.item} (${item.size})  $${item.price}`;

    addons = document.getElementsByName("sub_option");
    for (i=0; i<addons.length; i++) {
      if (addons[i].checked == true) {
        addons_text += `</br>+ ${addons[i].value} $${addons[i].dataset.addon_price}`;
        total_line_price += Number(addons[i].dataset.addon_price);
      }
    }

    total_text = `</br>Item Total: $${total_line_price.toFixed(2)}`;
    s_line.innerHTML = item_text + addons_text + total_text;

  } else if (item.category == "Dinner Platter") {
    s_line.innerHTML = `${item.category}:${item.item} (${item.size}) // Price: ${item.price}`;

  } else {
    s_line.innerHTML = `${item.category}:${item.item} // Price: ${item.price}`;
  }

  update_order_line(item);

} // update_item_display()

// updated the carts order line variable with item argument supplied
function update_order_line(item) {
  cart = get_cart();
  cur_order_line = cart_cur_line(cart);

  cur_order_line.category = item.category;
  cur_order_line.item = item.item;
  cur_order_line.item_price = item.price;
  cur_order_line.size = item.size;
  cur_order_line.toppings_opt = item.toppings_opt;
  cur_order_line.toppings_desc = item.toppings_desc;
  cur_order_line.toppings_list = get_selected_pizza_toppings();
  cur_order_line.total_line_price = Number(item.price);

  //build sub-options dictionary --> e.g. {"mushrooms":"0.50", :Green Peppers":"0.50"}
  cur_order_line.sub_options_list = []
  addons = document.getElementsByName("sub_option");
  for (i=0; i<addons.length; i++) {
    if (addons[i].checked == true) {
      cur_order_line.sub_options_list.push(addons[i].value);
      cur_order_line.total_line_price += Number(addons[i].dataset.addon_price);
    }
  }
  set_cart(cart);

} // end update_order_line()


// clears all selections in modal - called when modal is cancelled
function clear_modal () {
  clear_menu_item();
  clear_size();
  document.getElementById('size_selection').hidden = true;
  clear_toppings();
  document.getElementById('toppings_group').hidden = true;
  clear_sub_options()
  document.getElementById("sub_options").hidden = true;
  document.getElementById('item_display').innerHTML = '';

  //TODO: cancel current order line from cart

} //end clear_modal()

// clear selected menu item
function clear_menu_item() {
  document.getElementById("menu_item_selection").selectedIndex = 0
} // end clear_menu_item()

//clear size selection
function clear_size() {
  size_radios = document.getElementsByClassName("selected_size")
  num_radios = size_radios.length;
  for (var i=0; i<num_radios; i++) {
    size_radios[i].checked = false
  }
} // end clear_size()

// clear selected toppings from the DOM
function clear_toppings() {
  var list = document.getElementById("selected_toppings")
  while (list.firstChild) {
    list.removeChild(list.firstChild);
  }
} // end clear_toppings()

//clear the HTML table in the cart
function clear_cart_table() {
  cart_table = document.getElementById('cart_table');
  while (cart_table.lastChild.className == "order_line") {
    cart_table.removeChild(cart_table.lastChild);
  }
  order_total = document.getElementById('order_total');
  order_total.innerHTML = 0;
} // end clear_cart_table()

// clear sub_options from the DOM
function clear_sub_options() {
  var sub_options = document.getElementById("sub_options")
  while (sub_options.firstChild) {
    sub_options.removeChild(sub_options.firstChild);
  }
} // end clear_toppings()

// create a table for the cart display with items in the cart
function refresh_cart_table() {
  cart = get_cart();

  //clear cart table and redraw it
  clear_cart_table();
  cart_table = document.getElementById('cart_table');

  for (line in cart.order_lines) {
    line_num = Number(line) + 1;
    append_cart_line(line_num, cart_get_line(line, cart), cart_table, cart);
  }

  order_total = document.getElementById('order_total');
  order_total.style.textAlign = "right";
  order_total.innerHTML = `$${cart.order_total.toFixed(2)}`;
  set_cart(cart);

} // end display_cart_table()

// helper function for refresh_cart_table - adds new cart line item
function append_cart_line(num, line, cart_table, cart) {

  row = document.createElement('tr');
  row.className = "order_line";
  row.id = `line_${line.line_id}`;
  line_num = document.createElement('td');
  item = document.createElement('td');
  options = document.createElement('td');
  subttl = document.createElement('td');
  price = document.createElement('td');

  if (line.size != '') {
    size = `(${line.size})`;
  } else {
    size = '';
  }

  // configure remove item button
  line_num.innerHTML = num;

  const remove_but = document.createElement('span');
  remove_but.className = "badge badge-pill badge-danger ml-2";
  remove_but.innerHTML = "&times;";
  remove_but.onclick = (it) => {
    cart = get_cart();
    line = cart_get_line(num-1, cart);
    cart_remove_line (line.line_id, cart);
  } // end remove button on click
  line_num.appendChild(remove_but);

  item.innerHTML = `${line.category}: ${line.item} ${size}`;

  if (item.category == "Pizza"){
      options.innerHTML = `${item.toppings.length} toppings`;
  } else {
    options.innerHTML = "";
  }

  subttl.innerHTML = "";
  price.innerHTML = `$${line.total_line_price.toFixed(2)}`;
  price.style.textAlign = "right";

  row.appendChild(line_num);
  row.appendChild(item);
  row.appendChild(options);
  row.appendChild(subttl);
  row.appendChild(price);

  cart_table.appendChild(row);

} // end append_cart_line()
