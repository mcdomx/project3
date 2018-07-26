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
        const sel_item = i.options[i.selectedIndex].value;

        get_menu_items.open('POST', '/get_menu_items');
        get_menu_items.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
        console.log(CSRF_TOKEN)

        //when request is completed
        get_menu_items.onload = () => {
          //extract JSON data from request
          // const response = JSON.parse(get_menu_items.responseText)
          const response = get_menu_items.responseText


          //if pizza - display size options and toppings options
          //if sub - display size options, extra cheese check box and
          //   if steak + cheese, the additional options check boxes
        } //end onload


        // Add data to send with request
        const data = new FormData();

        data.append('sel_item', sel_item);

        // Send request
        get_menu_items.send(data);
        return false; // avoid sending the form and creating an HTTP POST request

  } // onchange for menu_item_selection

} // end setup_order_modal()
