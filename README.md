# Recipe-Wizard

## Login Page

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/loginpage.png?raw=true "Recipe Wizard Login Page")

  All unauthenticated users will be automatically redirected to this page upon visiting the site or any of its subdirectories. Here, they can input a username and a password. Upon pressing submit, this information will be sent to the server, where the authentication process will begin.
  
  First, the server will check if the username matches any accounts in the database. If so, it will check if the account has been locked due to too many failed login attempts. If it has, then authentication will stop here, the page will refresh, and the following message will be displayed along the top of the screen.

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/accountlocked.png?raw=true "Text box which displays: This account is locked due to too many failed login attempts. Please try again later.")

  In this situation, the user’s account will be locked for five minutes. After this time has passed, the account will no longer be locked.
  
  If the account is not locked, then the server will attempt to authenticate the user’s credentials. Password authentication is performed by the Django framework backend, which uses a PBKDF2 algorithm with a SHA256 hash.
  If the user’s credentials are valid, then they will be logged in and promptly redirected to the site’s landing page. Otherwise, the user’s failed login attempt counter will be incremented, the page will refresh, and the following error message will appear.

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/invalid.png?raw=true "Text box which displays: Invalid username or password.")

  The failed login counter increments by one for each failed login attempt. If the time passed since the last failed login attempt is greater than five minutes, then the counter will be reset.
  
## Register Page

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/registerpage.png?raw=true "Recipe wizard account registration page.")
  
  On this page, new users can register for an account. Every textbox must be filled in, or the submit button will not work. Once the form is submitted, this information will be sent to the server, where server-side validation will begin.
  
  First, the system will check to see if the username has been taken. If so, page will refresh and notify the user as such.
  
  Next, the system will verify that the email address is in the correct format. If not, then the registration process will not continue, and the user will be notified of the error.
  
  Finally, the system will verify that the contents of each password field match. If they do not, then the user will be notified as such, and the registration process will not continue.
  
  If all input is valid, then the system will create the account. The user will be redirected to the login page, where they will be shown a success message letting them know that their account has been created and that they can now log in to it.
  
## Landing Page

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/landingpage.png?raw=true "Recipe wizard landing page. Ten recipes are shown in a top-down list. Pages can be navigated with buttons along the bottom of the page.")

  This is the site’s landing page. You can only view this page as an authenticated user. Here, one can browse every recipe that the system has saved. Clicking on a recipe will redirect you to that recipe’s page. Pressing the next button will navigate to the next page, as pictured below.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/landingpage_page2.png?raw=true "Page 2 of the Recipe Wizard landing page. Ten different recipes are shown in the same format.")

  The “Prev” and “Next” buttons will only appear if a previous or a next page exists, respectively.
  Searches can be performed by inputting a query into the textbox at the top of the page and pressing Enter on your keyboard. This will redirect you to a page containing search results matching your query.

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/searchresults.png?raw=true "Recipe wizard landing page search results. Recipes matching the search query are displayed in a paginated view of ten per page.")

  The pagination here functions the same as on the landing page: the “Prev” and “Next” buttons will only appear when applicable. Clicking on any recipe will redirect you to that recipe’s page. The search bar on this page functions identically to the one on the landing page.
  
## My Cookbook

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mycookbook.png?raw=true "Recipe wizard cookbook page. Recipes are displayed in a paginated view of ten per page top to bottom in a list format.")

  On the My Cookbook page, one can view any recipes they have saved. This page is functionally the same as the landing page, the main difference being how the content is populated. The pagination works the same way, and clicking on a recipe will redirect you to its page. Using the search function will only display results from the user’s saved recipes, rather than from the entire database.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mycookbook_searchresults.png?raw=true "Recipe wizard cookbook search results page. Recipes are displayed in a paginated view of ten per page top to bottom in a list format.")

  This page functions identically to the landing page’s search results page, except the search bar at the top of the screen displays results from the user’s cookbook.
  
## My Kitchen

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen.png?raw=true "Recipe wizard kitchen inventory page. Buttons along the top of the page, in order, are Add, Delete Selected, and Save. Below these buttons is a table which displays all ingredients saved to the users accounts.")

  The My Kitchen page allows you to add, edit, and delete ingredients from your kitchen inventory. Your current inventory is displayed in a table. Each ingredient’s amount can be edited, and then saved by pressing the save button at the top. Pressing “Save” will submit your changes to the server, and reload the page.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen_ingredientselect.png?raw=true "Recipe wizard kitchen inventory page. The first and third rows of the ingredients table are selected.")

  You can click on the checkbox beside each row to select the ingredient displayed on it. Clicking “Delete Selected” will display the following popup.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen_deleteall.png?raw=true "A popup window titled 'Are you sure?'. The body of the window says, 'Are you sure you want to delete all selected items?'. There are two buttons along the bottom. The first says Cancel, the second says I'm Sure.")

  Pressing “Cancel” will close the popup without making any changes. Pressing “I’m Sure” will send a request to the server with the items to be deleted. The page will then be refreshed, and the deleted items will no longer appear on the page, as pictured below.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen_updatedingredients.png?raw=true "This image shows the ingredients table sans the rows which had previously been selected.")

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen_addingredient.png?raw=true "This image shows a popup window with two textboxes, an a dropdown menu. The first textbox is labelled 'Ingredient'. The second textbox is labelled 'Amount'. The dropdown is labelled 'Unit'. There are two buttons along the bottom. The first button is labelled 'Close'. The second button is labelled 'Submit'.")

  Clicking the “Add” button will display the above popup. You can then input an ingredient by name, amount, and select the unit of measurement you would like to use from the “Unit” dropdown.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/mykitchen_units.png?raw=true "This image shows the possible selections for the 'Unit' dropdown menu.")

  Once the user clicks submit, the form will be validated. The “Amount” textbox must contain a valid decimal number. The “Ingredient” textbox must not be empty, and a unit must have been selected. If everything is valid, then the form will be submitted. The page will then refresh, and the new ingredient will be added to the user’s kitchen.
  
## My Shopping List

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/shoppinglist.png?raw=true "Recipe Wizard shopping list page. There are four buttons along the top of the page. In order, these are Add, Clear, Delete Selected, and Save. Ingredients saved to the user's shopping list are displayed below in a table.")

  The My Shopping List page allows you to edit and add to your shopping list. It can either be automatically added to via recipe pages, or added to manually from this page. Ingredients can be edited in the same way as on the My Kitchen page, and the “Add” button functions the same way as well.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/shoppinglist_clear.png?raw=true "A popup window titled 'Are you sure?'. The body of the window reads, 'Are you sure you want to clear your shopping list? This action cannot be reversed. Buttons along the bottom read, Cancel, and I'm Sure.")

  Clicking the “Clear” button will display this popup. Pressing “Cancel” will close the popup without making any changes to the shopping list. Pressing “I’m Sure” will send a request to the server to clear the user’s shopping list. The page will then be refreshed, and the shopping list will be empty.
  
## My Account

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount.png?raw=true "Recipe Wizard Account page. The authenticated user's username, email, and password can be edited from this page.")

  My Account shows information about the currently authenticated account, and is the place to update information about your account. The text boxes on this page display the user’s username and email address. The password box always contains eight asterisks regardless of the length of your password, and is only there for aesthetic reasons.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount_username.png?raw=true "A popup window titled 'Update Username'. The body of the window contains a single textbox labelled 'New Username'.")

  Pressing the “Update” button next to your username will bring up this window. Entering a username into the “New Username” textbox will submit the query to the server and reload the page. If the username is taken, then no changes will be made, and an error message will display once the page reloads. Otherwise, your username will be changed, and a success message will appear.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount_username_updated.png?raw=true "An image showing the account page but with the user's updated username.")

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount_email.png?raw=true "A popup window titled 'Update Email address'. The body of the window contains three textboxes. The first is labelled 'Old Email'. The second is labelled 'New Email'. The third is labelled 'Confirm New Email'.")

  Clicking the “Update” button next to your email will display this popup. You must enter  your old email address into the box as a verification measure. Additionally, your new email must be entered into both the “New Email” textbox and the “Confirm New Email” textbox. If their contents do not match, then pressing the submit button will not work, and an error message will show. The contents of every textbox must be a valid email address. The form cannot be submitted otherwise.
  
  Once all input has been validated, an update query is sent to the server. The server then validates all inputs once more. If all checks are passed, then the user’s email address will be updated and the page will refresh.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount_email_updated.png?raw=true "An image showing the account page but with the user's updated email address.")

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/myaccount_password.png?raw=true "A popup window titled 'Update Password'. The body of the window contains three textboxes. The first is labelled 'Old Password'. The second is labelled 'New Password'. The third is labelled 'Confirm New Password'.")

  This popup appears when the “Update” button on the password row is pressed. You must input your old password in the top textbox as a verification step. Then, the new password must be inputted twice into the bottom two textboxes. If they do not match, then the form cannot be submitted, and the same error message as the one in the email popup will show. Once all client-side verification checks have passed, an update query will be sent to the server.
  First, the server will verify that the old password is correct. If it is not, then processing will stop here, the page will refresh, and an error message will show. If the password matches, then the server will make sure that both “New Password” inputs match. If they do not, then the page will refresh, and an error message will appear. Otherwise, the user’s password will be updated, they will be logged out, and redirected to the login page.

## Recipe Page

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/recipepage.png?raw=true "Recipe Wizard recipe page.")

  The recipe page shows information about a given recipe. Next to the title on the top is the “Save” button. Clicking it will either save or un-save the recipe. Saved recipes appear on the “My Cookbook” page.
  Clicking the link below the image will redirect you to the website on which this recipe originated.

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/recipepage_ingredients.png?raw=true "A table showing the ingredients involved in a recipe. The first and third rows are highlighted in red.")

  The serving count textbox allows you to change the proportions of the recipe. When the serving count is changed, the amounts of each ingredient will update proportionally.
  Ingredients will be highlighted red if the user does not have it listed on their My Kitchen page. This serves as an indicator of whether or not they are able to prepare the recipe with their current stock. 

![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/recipepage_addalias.png?raw=true "A popup window titled 'Add Alias'. The body contains a single dropdown menu titled 'Alias'.")

The dropdown menu on the side of each row will show an option called “Add Alias”. Clicking on that will bring up this menu. Clicking on the “Alias” dropdown will show a list of names pulled from the user’s kitchen inventory. This allows you to let the system know that two ingredients are equivalent. For example: if a recipe calls for hot sauce, but you have Frank’s hot sauce listed in your kitchen, you can submit this form to let the system know that hot sauce and Frank’s hot sauce should be considered equivalent. Then, whenever the system queries the database for hot sauce, it will come up with Frank’s hot sauce.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/recipepage_ingredientsadded.png?raw=true "A popup window titled 'Missing ingredients added'. The body reads, 'Missing ingredients have been successfully added to your shopping list.")
  
  Clicking the “Add missing ingredients to shopping list” button will send a query to the server containing all rows highlighted in red. These ingredients will then be added to your shopping list. Pressing “Ok” will redirect you to the My Shopping List page, where you can see the ingredients have been added.
  
![Alt text](https://github.com/Exo2986/Recipe-Wizard/blob/master/readme_images/recipepage_markcooked.png?raw=true "A popup window titled 'Mark as Cooked'. The body contains a single text boxese labelled 'Serving Count'.")

This menu appears whenever the “Mark recipe as cooked” is pressed. Inputting a numerical serving count here and pressing “Submit” will send a query to the server containing every ingredient in the recipe updated proportionally to the serving count. The server will then convert the recipe ingredient units to the kitchen ingredient units, and deduct all of these amounts from the amounts present in the user’s kitchen. If the leftover amount is less than 0.01, then that kitchen ingredient entry will be removed. The user will then be redirected to the My Kitchen page.
