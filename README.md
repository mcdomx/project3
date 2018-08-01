# Project 3

## Summary
The landing page is a static menu.  If the user is not logged in, no "order" button is available.  If the user is logged in and the user is a superuser, the "Order Status Maintenance" button is also available.  If the user has a previous cart available, the items are loaded into the cart.

New users can register with the "Register" button.

When clicking the "Order" button, a modal window is presented with menu items in a drop down.  Depending on the item selected, various options will be presented for the user to choose from.  The user can add and remove pizza toppings.  When toppings are added, they are no longer available to be added, but if they are removed from the pizza, they re-appear on the drop down list.  If the user switches betweeb pizza tyoes, the toppings are retained, but if the user switches to a different menu type, the toppings are cleared.  Sub addons can be freely added or removed.  When options are added or removed, the subtotal at the bottom of the window updates.

When the item is finalized, "Add to Cart" can be clicked which will dismissing the window and update the header with the number of items in the cart and a "View Cart" button is shown.  Viewing the cart gives the user the option to remove items or place the order.  When the order is placed, a confirmation will be presented to the user with an order number and amount.  All orders are only configured for pickup.

A superuser can change the status of all non-complete orders with a drop down box.

## Models
The model is based on the Menu_items.  Each entry in this table is intended to be a unique price point without special additions.  This avoids the need for subtables to determine pricing.  Sub addons are calculated outside of the menu table.

Tables for Order_lines and Orders are heavily used and have dictionary methods to communicate back to the client.  __str__ functions are configured for display in the Admin interface.

In most tables an "available" option is saved.  I intended to make all items flexible so that only avilable items were presented to the user, but I was unable to completely implement this functionality.  However, items can be added or removed from the menu through the admin interface so they are not available for ordering.  Since the menu page is static, they will not be updated on the main menu page.  

During the build, I made some changes to the model after understanding how both Javascipt, Django and Python worked together and ran into some problems with nested dictionaries and JSON.  I had to make some changes to the model to support some of the limitations that I encountered.  There is a class and an order_lines class in Javascipt which I may not have needed, but were useful in my initial design.

I had numerous glitches loading data from my load_menu.py file.  The loads work and I used them extensively, but on occasion, data refused to load completely.  I could not find the source of the problem but was able to get the data loaded successfully.  I did make some changes to the data after loading it and added a table for status that does not have a load option because it was so small.  

## Admin
The admin module is somewhat extensively configured.  Additional configuration was necessary to allow orders and order lines to be properly displayed with the "related_names" setting.  

## Channels
I did not configure Channels to be used with this application.  The only place where this would have been reasonable was in the Order Status Maintenance page, but I didn't have the time to add this.  

##  Javascript
This application is heavily Javascript dependent.  Extensive use of AJAX is used to communicate with the server end of the application.  The js file is heavily refactored.  If I had more time, this file could be cleaned up and streamlined better, but I simply ran out of time.  There is a separate js file for the order maintenance and for the main index page.  I did this to try to keep the file from getting too long.  There is a lot of functionality, so there are a lot of functions.  

## Django Templating
I used Django's HTML templating in order to create the order maintenance page as well as the basic layout.

## Cart Persistence
This was a challenge for me.  I had problems with getting django and javascript to work well together and using JSON did not always work as I expected.  I tried to make the cart a session object, but getting the data to transfer cleanly between the client and the server proved problematic.  I ended up with using localStorage.

## Conclusion
I am not sure why I had such a problem with this project.  I am usually good at data structures, but the Django modeling caused me some confusion.  I wasn't really sure what was possible and how it would respond.  That took a while to figure out.  This is probably why I leaned so heavily on the client side to get things done for this project.  I did like the user authentication process with Django, but frankly, I am not entirely sure how it works.  Django is a complex tool of which I only used the basis.


Citations:
Used this site to learn how to create register, login and logout forms
https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
