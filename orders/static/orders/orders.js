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

        var i = document.getElementById("menu_item_selection");
        // use text instead of value to get text including spaces
        const sel_item = i.options[i.selectedIndex].text;

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
          if (response[0].size != '') {
            document.querySelector('#size_selection').hidden = false;
          }

          if (response[0].category_id == 'Pizza') {
            // load pizza toppings into drop down menu
            load_pizza_toppings()
          }

          //if sub - display size options, extra cheese check box and
          //   if steak + cheese, the additional options check boxes
        } //end onload

        // Add data to send with request
        const data = new FormData();

        data.append('sel_item', sel_item);

        get_menu_items.send(data); // Send request
        return false; // avoid sending the form

  } // onchange for menu_item_selection

  document.querySelector('#selected_toppings').onclick = () => {
    get_slected_pizza_toppings()
  }

} // end setup_order_modal()

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
            // parent = document.getElementById("selected_toppings");
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

      document.querySelector('#toppings_group').hidden = false;

    } // end onload

    // Send request
    get_toppings.send();
    return false; // avoid sending the form and creating an HTTP POST request
}

function get_slected_pizza_toppings() {
    elements = document.getElementsByClassName('selected_pizza_toppings');
    rv = []
    for (i=0; i<elements.length; i++) {
      rv.push(elements[i].id);
    }
    return rv;
    // elements.forEach(list_item)

function count_slected_pizza_toppings() {
  elements = document.getElementsByClassName('selected_pizza_toppings');
  return elements.length;
}


} // end get_slected_pizza_toppings

function list_item (item, index) {
  console.log(item)
} // list_item
