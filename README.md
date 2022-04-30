## Login Page

![](RackMultipart20220430-1-ew59h6_html_f612873b7fc46856.png)

All unauthenticated users will be automatically redirected to this page upon visiting the site or any of its subdirectories. Here, they can input a username and a password. Upon pressing submit, this information will be sent to the server, where the authentication process will begin.

First, the server will check if the username matches any accounts in the database. If so, it will check if the account has been locked due to too many failed login attempts. If it has, then authentication will stop here, the page will refresh, and the following message will be displayed along the top of the screen.

![](RackMultipart20220430-1-ew59h6_html_a4272b7039b8e2e8.png)

In this situation, the user&#39;s account will be locked for five minutes. After this time has passed, the account will no longer be locked.

If the account is not locked, then the server will attempt to authenticate the user&#39;s credentials. Password authentication is performed by the Django framework backend, which uses a PBKDF2 algorithm with a SHA256 hash.

If the user&#39;s credentials are valid, then they will be logged in and promptly redirected to the site&#39;s landing page. Otherwise, the user&#39;s failed login attempt counter will be incremented, the page will refresh, and the following error message will appear.

![](RackMultipart20220430-1-ew59h6_html_d7d5fb99967202bf.png)

The failed login counter increments by one for each failed login attempt. If the time passed since the last failed login attempt is greater than five minutes, then the counter will be reset.

## Register Page

![](RackMultipart20220430-1-ew59h6_html_72d304ba3813950f.png)

On this page, new users can register for an account. Every textbox must be filled in, or the submit button will not work. Once the form is submitted, this information will be sent to the server, where server-side validation will begin.

First, the system will check to see if the username has been taken. If so, page will refresh and notify the user as such.

Next, the system will verify that the email address is in the correct format. If not, then the registration process will not continue, and the user will be notified of the error.

Finally, the system will verify that the contents of each password field match. If they do not, then the user will be notified as such, and the registration process will not continue.

If all input is valid, then the system will create the account. The user will be redirected to the login page, where they will be shown a success message letting them know that their account has been created and that they can now log in to it.

## Landing Page

![](RackMultipart20220430-1-ew59h6_html_6bd8ffa901ff2f28.png)

This is the site&#39;s landing page. You can only view this page as an authenticated user. Here, one can browse every recipe that the system has saved. Clicking on a recipe will redirect you to that recipe&#39;s page. Pressing the next button will navigate to the next page, as pictured below.

![](RackMultipart20220430-1-ew59h6_html_c37e08fde6bc7769.png)

The &quot;Prev&quot; and &quot;Next&quot; buttons will only appear if a previous or a next page exists, respectively.

Searches can be performed by inputting a query into the textbox at the top of the page and pressing Enter on your keyboard. This will redirect you to a page containing search results matching your query.

![](RackMultipart20220430-1-ew59h6_html_491b8b2cfde81b99.png)

The pagination here functions the same as on the landing page: the &quot;Prev&quot; and &quot;Next&quot; buttons will only appear when applicable. Clicking on any recipe will redirect you to that recipe&#39;s page. The search bar on this page functions identically to the one on the landing page.

## My Cookbook

![](RackMultipart20220430-1-ew59h6_html_b0fffc09ac292d81.png)

On the My Cookbook page, one can view any recipes they have saved. This page is functionally the same as the landing page, the main difference being how the content is populated. The pagination works the same way, and clicking on a recipe will redirect you to its page. Using the search function will only display results from the user&#39;s saved recipes, rather than from the entire database.

![](RackMultipart20220430-1-ew59h6_html_ba69a10e23152ba4.png)

This page functions identically to the landing page&#39;s search results page, except the search bar at the top of the screen displays results from the user&#39;s cookbook.

## My Kitchen

![](RackMultipart20220430-1-ew59h6_html_94f94d278b457df2.png)

The My Kitchen page allows you to add, edit, and delete ingredients from your kitchen inventory. Your current inventory is displayed in a table. Each ingredient&#39;s amount can be edited, and then saved by pressing the save button at the top. Pressing &quot;Save&quot; will submit your changes to the server, and reload the page.

![](RackMultipart20220430-1-ew59h6_html_2ca663fc7ee355b2.png)

You can click on the checkbox beside each row to select the ingredient displayed on it. Clicking &quot;Delete Selected&quot; will display the following popup.

![](RackMultipart20220430-1-ew59h6_html_a9852b1a826d679c.png)

Pressing &quot;Cancel&quot; will close the popup without making any changes. Pressing &quot;I&#39;m Sure&quot; will send a request to the server with the items to be deleted. The page will then be refreshed, and the deleted items will no longer appear on the page, as pictured below.

![](RackMultipart20220430-1-ew59h6_html_1ce3c8ea8d679017.png)

![](RackMultipart20220430-1-ew59h6_html_dd23df0295503125.png)

Clicking the &quot;Add&quot; button will display the above popup. You can then input an ingredient by name, amount, and select the unit of measurement you would like to use from the &quot;Unit&quot; dropdown.

![](RackMultipart20220430-1-ew59h6_html_61e5e8f488c4a52d.png)

Once the user clicks submit, the form will be validated. The &quot;Amount&quot; textbox must contain a valid decimal number. The &quot;Ingredient&quot; textbox must not be empty, and a unit must have been selected. If everything is valid, then the form will be submitted. The page will then refresh, and the new ingredient will be added to the user&#39;s kitchen.

![](RackMultipart20220430-1-ew59h6_html_5707f942a2b85d96.png)

![](RackMultipart20220430-1-ew59h6_html_5919abe0bd08189.png)

## My Shopping List

![](RackMultipart20220430-1-ew59h6_html_404cfa1c57206e67.png)

The My Shopping List page allows you to edit and add to your shopping list. It can either be automatically added to via recipe pages, or added to manually from this page. Ingredients can be edited in the same way as on the My Kitchen page, and the &quot;Add&quot; button functions the same way as well.

![](RackMultipart20220430-1-ew59h6_html_202d63ae33fd7ebd.png)

Clicking the &quot;Clear&quot; button will display this popup. Pressing &quot;Cancel&quot; will close the popup without making any changes to the shopping list. Pressing &quot;I&#39;m Sure&quot; will send a request to the server to clear the user&#39;s shopping list. The page will then be refreshed, and the shopping list will be empty.

## My Account

![](RackMultipart20220430-1-ew59h6_html_ea2675a5a7015cd7.png)

My Account shows information about the currently authenticated account, and is the place to update information about your account. The text boxes on this page display the user&#39;s username and email address. The password box always contains eight asterisks regardless of the length of your password, and is only there for aesthetic reasons.

![](RackMultipart20220430-1-ew59h6_html_791cd4cb3b201626.png)

Pressing the &quot;Update&quot; button next to your username will bring up this window. Entering a username into the &quot;New Username&quot; textbox will submit the query to the server and reload the page. If the username is taken, then no changes will be made, and an error message will display once the page reloads. Otherwise, your username will be changed, and a success message will appear.

![](RackMultipart20220430-1-ew59h6_html_ec9a6da4c8734bf7.png)

![](RackMultipart20220430-1-ew59h6_html_e8ef8e35f7e30906.png)

Clicking the &quot;Update&quot; button next to your email will display this popup. You must enter your old email address into the box as a verification measure. Additionally, your new email must be entered into both the &quot;New Email&quot; textbox and the &quot;Confirm New Email&quot; textbox. If their contents do not match, then pressing the submit button will not work, and an error message will show. The contents of every textbox must be a valid email address. The form cannot be submitted otherwise.

![](RackMultipart20220430-1-ew59h6_html_59e949bfeda9d696.png)

Once all input has been validated, an update query is sent to the server. The server then validates all inputs once more. If all checks are passed, then the user&#39;s email address will be updated and the page will refresh.

![](RackMultipart20220430-1-ew59h6_html_ab023be1d894d42b.png)

![](RackMultipart20220430-1-ew59h6_html_dc26f7477fe8967a.png)

This popup appears when the &quot;Update&quot; button on the password row is pressed. You must input your old password in the top textbox as a verification step. Then, the new password must be inputted twice into the bottom two textboxes. If they do not match, then the form cannot be submitted, and the same error message as the one in the email popup will show. Once all client-side verification checks have passed, an update query will be sent to the server.

First, the server will verify that the old password is correct. If it is not, then processing will stop here, the page will refresh, and an error message will show. If the password matches, then the server will make sure that both &quot;New Password&quot; inputs match. If they do not, then the page will refresh, and an error message will appear. Otherwise, the user&#39;s password will be updated, they will be logged out, and redirected to the login page.

## Recipe Page

![](RackMultipart20220430-1-ew59h6_html_c5f7817ef6764d31.png)

The recipe page shows information about a given recipe. Next to the title on the top is the &quot;Save&quot; button. Clicking it will either save or un-save the recipe. Saved recipes appear on the &quot;My Cookbook&quot; page.

Clicking the link below the image will redirect you to the website on which this recipe originated.

![](RackMultipart20220430-1-ew59h6_html_91552cd063cbd936.png)

The serving count textbox allows you to change the proportions of the recipe. When the serving count is changed, the amounts of each ingredient will update proportionally.

Ingredients will be highlighted red if the user does not have it listed on their My Kitchen page. This serves as an indicator of whether or not they are able to prepare the recipe with their current stock.

![](RackMultipart20220430-1-ew59h6_html_568406dace162e40.png)

The dropdown menu on the side of each row will show an option called &quot;Add Alias&quot;. Clicking on that will bring up this menu. Clicking on the &quot;Alias&quot; dropdown will show a list of names pulled from the user&#39;s kitchen inventory. This allows you to let the system know that two ingredients are equivalent. For example: if a recipe calls for hot sauce, but you have Frank&#39;s hot sauce listed in your kitchen, you can submit this form to let the system know that hot sauce and Frank&#39;s hot sauce should be considered equivalent. Then, whenever the system queries the database for hot sauce, it will come up with Frank&#39;s hot sauce.

![](RackMultipart20220430-1-ew59h6_html_be623160f8bacc7.png)

Clicking the &quot;Add missing ingredients to shopping list&quot; button will send a query to the server containing all rows highlighted in red. These ingredients will then be added to your shopping list. Pressing &quot;Ok&quot; will redirect you to the My Shopping List page, where you can see the ingredients have been added.

![](RackMultipart20220430-1-ew59h6_html_97455c8da71ce604.png)

This menu appears whenever the &quot;Mark recipe as cooked&quot; is pressed. Inputting a numerical serving count here and pressing &quot;Submit&quot; will send a query to the server containing every ingredient in the recipe updated proportionally to the serving count. The server will then convert the recipe ingredient units to the kitchen ingredient units, and deduct all of these amounts from the amounts present in the user&#39;s kitchen. If the leftover amount is less than 0.01, then that kitchen ingredient entry will be removed. The user will then be redirected to the My Kitchen page.
