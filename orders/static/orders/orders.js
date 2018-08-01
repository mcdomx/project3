
// #############  CLASSES  #############

class Order_line {
  constructor (category, item, size, item_price, toppings_opt, toppings_desc, toppings_list, sub_options_list, ttl_price) {
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

  //create a blank new line
  new_line () {
    this.order_lines.push(new Order_line());
  }

  recalc_total () {
    this.order_total = 0;
    for (i in this.order_lines) {
      this.order_total += this.get_line(i).total_line_price;
    }
    //update number of cart items in header
    document.getElementById('num_cartitems').innerHTML = this.num_items();

  } // end recalc_total()

  //update total of line
  add_cur_line () {
    this.recalc_total();
    line_in_process = false;
  }

  cur_line () {
    return this.order_lines[ cart.order_lines.length - 1 ];
  }

  get_line (line_num) {
    return this.order_lines[line_num];
  }

  num_items () {
    return this.order_lines.length;
  }

  //TODO: i think this can be deleted - doesn't appear to be used
  remove (line_id) {
    for (line in this.order_lines)
      if (this.order_lines[line].line_id == line_id){
        this.order_lines.splice(line,1);
        this.recalc_total();
        return;
      }
  }

  clear_cart () {
    //remove items from cart
    for (line in this.order_lines){
      this.order_lines.splice(line, 1);
    }
    this.order_total = 0;

    //clear the shopping cart display
    clear_cart_table()

    //update number of cart items in header
    document.getElementById('num_cartitems').innerHTML = 0;

  }
} // end CLASS CART

// #############  END CLASSES  #############


// #############  GLOBAL VARIABLES  #############

toppings_list_populated = false;
cart = new Cart();
line_in_process = false;

// #############  END GLOBAL VARIABLES  #############


// ########################  begin DOMContentLoaded ########################
document.addEventListener('DOMContentLoaded', () => {

  setup_order_modal();

});
// ########################  end DOMContentLoaded ########################

function setup_order_modal () {

  document.getElementById('menu_item_selection').onchange = refresh_modal;
  document.getElementById('size_selection').onchange = update_modal;
  document.getElementById('btn_add_to_cart').onclick = add_to_cart;
  document.getElementById('btn_place_order').onclick = place_order;
  document.getElementById('btn_delete_cart').onclick = cart.clear_cart();


  document.getElementById('btn_close_success').onclick = () => {
    s_modal = document.getElementById('order_success_modal');
    s_modal.style.display="none";
  }


  //TODO: make sure this btn is only enabled when there is a full item to order

  document.getElementById('cancel_modal').onclick = () => {
    clear_modal();
  }

} // end setup_order_modal()


function place_order() {
  submit_order_to_server();

} // end place_order()

// send current cart to server
function submit_order_to_server() {

  const place_order = new XMLHttpRequest();
  place_order.open('POST', '/place_order');
  place_order.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

  //when request is completed
  place_order.onload = () => {

    const message = JSON .parse(place_order.responseText)
    cart.clear_cart();
    display_order_success_modal(message);

  } //end onload

  // Add data to send with request
  const data = new FormData();

  data.append('cart', JSON.stringify(cart));

  place_order.send(data); // Send request
  return false; // avoid sending the form


} // end place_order

function display_order_success_modal(message) {
  console.log(message)
  o_number = document.getElementById('order_number')
  o_number.innerHTML = message["order_number"];

  o_total = document.getElementById('order_ttl')
  ttl = Number(message["order_total"]).toFixed(2)
  o_total.innerHTML = `$${ttl}`;


  $("#order_success_modal").modal();
}


// get selections from modal --  create order line -- add line to cart
function add_to_cart() {
  cart.add_cur_line();
  clear_modal();
  create_cart_table();
} // end add to cart

function refresh_modal() {
  draw_modal(initial_modal);
}

function update_modal() {
  draw_modal(update_line_summary);
}

// gets a menu item from the server based on user selections
// updates the modal with options based on user selection
// will also update the price
function draw_modal(modal_function) {

      if (line_in_process == false) {
        cart.new_line();
        line_in_process = true;
      }

      //initialize new request
      const get_menu_items = new XMLHttpRequest();
      const sel_item = get_selected_menu_item().item;
      const sel_cat = get_selected_menu_item().category;
      const sel_size = get_selected_size();
      const sel_toppings_list = get_selected_pizza_toppings();
      const sel_subOptions = get_selected_subOptions();


      get_menu_items.open('POST', '/get_menu_items');
      get_menu_items.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

      //when request is completed
      get_menu_items.onload = () => {
        //extract JSON data from request
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
function initial_modal(item) {

  document.querySelector('#size_selection').hidden = true;
  document.querySelector('#toppings_group').hidden = true;
  document.querySelector('#sub_options').hidden = true;

  // If item has size option, show size
  if (item.size != 'NA') {
    document.querySelector('#size_selection').hidden = false;
  } else {  //otherwise, clear the size selection and hide it
    // clear_size();
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

function get_selected_menu_item () {
    var i = document.getElementById("menu_item_selection");
    i_text = i.options[i.selectedIndex].text;
    i_split = i_text.split(':');
    category = i_split[0];
    item = i_split[1].trim();
    return {"category":category, "item":item};
}

// get the selected size.  return false if neither is selected
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


function get_selected_pizza_toppings() {
    elements = document.getElementsByClassName('selected_pizza_toppings');
    rv = []
    for (i=0; i<elements.length; i++) {
      rv.push(elements[i].id);
    }
    return rv;
} // end get_selected_pizza_toppings


function count_selected_pizza_toppings() {
  elements = document.getElementsByClassName('selected_pizza_toppings');
  return elements.length;
} // end count_slected_pizza_toppings()


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


// update the menu item selection and price
function update_line_summary(item) {

  s_line = document.getElementById('item_display');

  //TODO: consider first updating the order line and then displaying results.  Wait till you have the order line working to do this.
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


function update_order_line(item) {

  cur_order_line = cart.cur_line();

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


function create_cart_table() {

  //clear cart table and redraw it
  clear_cart_table();
  cart_table = document.getElementById('cart_table');

  for (line in cart.order_lines) {
    line_num = Number(line) + 1;
    append_cart_line(line_num, cart.get_line(line), cart_table);
  }

  order_total = document.getElementById('order_total');
  order_total.style.textAlign = "right";
  order_total.innerHTML = `$${cart.order_total.toFixed(2)}`;

} // end display_cart_table()




function append_cart_line(num, line, cart_table) {

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
  remove_but.onclick = () => {
    cart.remove(line.line_id);
    create_cart_table();
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
