
toppings_list_populated = false;

// ########################  begin DOMContentLoaded ########################
document.addEventListener('DOMContentLoaded', () => {

  // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  // //
  // socket.on('connect', () => {
  //   alert("socket established")
  //
  // }); // end on connect

  setup_order_modal();

});
// ########################  end DOMContentLoaded ########################

function setup_order_modal () {

  document.querySelector('#menu_item_selection').onchange = () => {



        //initialize new request
        const get_menu_items = new XMLHttpRequest();
        const sel_item = get_selected_menu_item();

        get_menu_items.open('POST', '/get_menu_items');
        get_menu_items.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

        //when request is completed
        get_menu_items.onload = () => {
          //extract JSON data from request
          const response = JSON.parse(get_menu_items.responseText)
          // response is a list of dictionary items each of which
          // represents a possible menu choice based on initial selection

          //if item has a size option, display selection
          // unhide id="size_selection"
          display_modal_options(response);

          // if (response[0].size != '') {
          //   document.querySelector('#size_selection').hidden = false;
          // }
          //
          // if (response[0].category_id == 'Pizza' && !toppings_list_populated) {
          //   // load pizza toppings into drop down menu
          //   load_pizza_toppings()
          // }

          //if sub - display size options, extra cheese check box and
          //   if steak + cheese, the additional options check boxes
        } //end onload

        // Add data to send with request
        const data = new FormData();

        data.append('sel_item', sel_item);

        get_menu_items.send(data); // Send request
        return false; // avoid sending the form

  } // onchange for menu_item_selection



  document.getElementById('cancel_modal').onclick = () => {
    clear_modal();
  }


} // end setup_order_modal()


function display_modal_options (items) {
  // start by hidding all items
  document.querySelector('#size_selection').hidden = true;
  document.querySelector('#toppings_group').hidden = true;

  if (items[0].size != '') {
    document.querySelector('#size_selection').hidden = false;
  } else {
    clear_size()
  }

  if (items[0].category_id == 'Pizza' ) {

    if (!toppings_list_populated) { load_pizza_toppings() }

    document.querySelector('#toppings_group').hidden = false;
  } else {
    clear_toppings()
  }
}

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
          remove_but.innerHTML = "-";
          remove_but.onclick = () => {
            // code to remove item from the list
            this_item = document.getElementById(topping);
            this_item.parentNode.removeChild(this_item);
          } // end remove button on click
          sel_item.appendChild(remove_but);

          // add selected item to list
          sel_toppings_list = document.getElementById("selected_toppings");
          sel_toppings_list.appendChild(sel_item);
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
    return i.options[i.selectedIndex].text;
}


function get_selected_pizza_toppings() {
    elements = document.getElementsByClassName('selected_pizza_toppings');
    rv = []
    for (i=0; i<elements.length; i++) {
      rv.push(elements[i].id);
    }
    return rv;

function count_slected_pizza_toppings() {
  elements = document.getElementsByClassName('selected_pizza_toppings');
  return elements.length;
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
  return false
} // end get_size()


} // end get_selected_pizza_toppings

// update the menu item selection and price
function update_item_display() {

  // toppings_list = document.getElementById("toppings_list");
  sel_item = get_selected_menu_item();
  sel_size = get_selected_size()
  toppings_count = count_selected_pizza_toppings();

  //TODO:  this is where I left offset
  //query menu to get the price
  //return a description to dom element


} // update_item_display()

// clears all selections in modal - called when modal is cancelled
function clear_modal () {
  clear_menu_item();
  clear_size();
  document.getElementById('size_selection').hidden = true;
  clear_toppings();
  document.getElementById('toppings_group').hidden = true;
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




// will get menu item based on arguments passed
function query_menu_item(kwargs) {

}
