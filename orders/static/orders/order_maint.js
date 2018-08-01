
// Javascript for the order_maint.html page

// ########################  begin DOMContentLoaded ########################
document.addEventListener('DOMContentLoaded', (evevnt) => {



});
// ########################  end DOMContentLoaded ########################

function update_status(value) {
  console.log(`Status updated: ${value}`);
  // value_str = JSON.stringify(value);
  // console.log(value_str)

  const change_status = new XMLHttpRequest();
  change_status.open('POST', '/change_status');
  change_status.setRequestHeader("X-CSRFToken", CSRF_TOKEN);

  value_split = value.split(':');

  //when request is completed
  change_status.onload = () => {

    const message = JSON.parse(change_status.responseText)
    console.log(message)

  } //end onload

  // Add data to send with request
  const data = new FormData();

  data.append('order_num', value_split[0]);
  data.append('new_status', value_split[1]);

  change_status.send(data); // Send request
  return false; // avoid sending the form

}
